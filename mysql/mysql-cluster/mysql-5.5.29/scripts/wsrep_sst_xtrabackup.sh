#!/bin/bash -ue
# Copyright (C) 2013 Percona Inc
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston
# MA  02110-1301  USA.

# Optional dependencies and options documented here: http://www.percona.com/doc/percona-xtradb-cluster/manual/xtrabackup_sst.html 
# Make sure to read that before proceeding!




. $(dirname $0)/wsrep_sst_common

ealgo=""
ekey=""
ekeyfile=""
encrypt=0
nproc=1
ecode=0
XTRABACKUP_PID=""
SST_PORT=""
REMOTEIP=""
tcert=""
tpem=""
sockopt=""
progress=""
ttime=0
totime=0
lsn=""
incremental=0
ecmd=""
rlimit=""

sfmt="tar"
strmcmd=""
tfmt=""
tcmd=""
rebuild=0
rebuildcmd=""
payload=0
pvformat="-F '%N => Rate:%r Avg:%a Elapsed:%t %e Bytes: %b %p' "
pvopts="-f  -i 10 -N $WSREP_SST_OPT_ROLE "
uextra=0

if which pv &>/dev/null && pv --help | grep -q FORMAT;then 
    pvopts+=$pvformat
fi
pcmd="pv $pvopts"
declare -a RC

INNOBACKUPEX_BIN=innobackupex
readonly AUTH=(${WSREP_SST_OPT_AUTH//:/ })
DATA="${WSREP_SST_OPT_DATA}"
INFO_FILE="xtrabackup_galera_info"
IST_FILE="xtrabackup_ist"
MAGIC_FILE="${DATA}/${INFO_FILE}"

# Setting the path for ss and ip
export PATH="/usr/sbin:/sbin:$PATH"

timeit(){
    local stage=$1
    shift
    local cmd="$@"
    local x1 x2 took extcode

    if [[ $ttime -eq 1 ]];then 
        x1=$(date +%s)
        wsrep_log_info "Evaluating $cmd"
        eval "$cmd"
        extcode=$?
        x2=$(date +%s)
        took=$(( x2-x1 ))
        wsrep_log_info "NOTE: $stage took $took seconds"
        totime=$(( totime+took ))
    else 
        wsrep_log_info "Evaluating $cmd"
        eval "$cmd"
        extcode=$?
    fi
    return $extcode
}

get_keys()
{
    if [[ $encrypt -eq 2 ]];then 
        return 
    fi

    if [[ $encrypt -eq 0 ]];then 
        if my_print_defaults -c $WSREP_SST_OPT_CONF xtrabackup | grep -q encrypt;then
            wsrep_log_error "Unexpected option combination. SST may fail. Refer to http://www.percona.com/doc/percona-xtradb-cluster/manual/xtrabackup_sst.html "
        fi
        return
    fi

    if [[ $sfmt == 'tar' ]];then
        wsrep_log_info "NOTE: Xtrabackup-based encryption - encrypt=1 - cannot be enabled with tar format"
        encrypt=0
        return
    fi

    wsrep_log_info "Xtrabackup based encryption enabled in my.cnf - Supported only from Xtrabackup 2.1.4"

    if [[ -z $ealgo ]];then
        wsrep_log_error "FATAL: Encryption algorithm empty from my.cnf, bailing out"
        exit 3
    fi

    if [[ -z $ekey && ! -r $ekeyfile ]];then
        wsrep_log_error "FATAL: Either key or keyfile must be readable"
        exit 3
    fi

    if [[ -z $ekey ]];then
        ecmd="xbcrypt --encrypt-algo=$ealgo --encrypt-key-file=$ekeyfile"
    else
        ecmd="xbcrypt --encrypt-algo=$ealgo --encrypt-key=$ekey"
    fi

    if [[ "$WSREP_SST_OPT_ROLE" == "joiner" ]];then
        ecmd+=" -d"
    fi
}

get_transfer()
{
    if [[ -z $SST_PORT ]];then 
        TSST_PORT=4444
    else 
        TSST_PORT=$SST_PORT
    fi

    if [[ $tfmt == 'nc' ]];then
        if [[ ! -x `which nc` ]];then 
            wsrep_log_error "nc(netcat) not found in path: $PATH"
            exit 2
        fi
        wsrep_log_info "Using netcat as streamer"
        if [[ "$WSREP_SST_OPT_ROLE"  == "joiner" ]];then
            tcmd="nc -dl ${TSST_PORT}"
        else
            tcmd="nc ${REMOTEIP} ${TSST_PORT}"
        fi
    else
        tfmt='socat'
        wsrep_log_info "Using socat as streamer"
        if [[ ! -x `which socat` ]];then 
            wsrep_log_error "socat not found in path: $PATH"
            exit 2
        fi

        if [[ $encrypt -eq 2 ]] && ! socat -V | grep -q OPENSSL;then 
            wsrep_log_info "NOTE: socat is not openssl enabled, falling back to plain transfer"
            encrypt=0
        fi

        if [[ $encrypt -eq 2 ]];then 
            wsrep_log_info "Using openssl based encryption with socat"
            if [[ -z $tpem || -z $tcert ]];then 
                wsrep_log_error "Both PEM and CRT files required"
                exit 22
            fi
            if [[ "$WSREP_SST_OPT_ROLE"  == "joiner" ]];then
                wsrep_log_info "Decrypting with PEM $tpem, CA: $tcert"
                tcmd="socat -u openssl-listen:${TSST_PORT},reuseaddr,cert=$tpem,cafile=${tcert}${sockopt} stdio"
            else
                wsrep_log_info "Encrypting with PEM $tpem, CA: $tcert"
                tcmd="socat -u stdio openssl-connect:${REMOTEIP}:${TSST_PORT},cert=$tpem,cafile=${tcert}${sockopt}"
            fi
        else 
            if [[ "$WSREP_SST_OPT_ROLE"  == "joiner" ]];then
                tcmd="socat -u TCP-LISTEN:${TSST_PORT},reuseaddr${sockopt} stdio"
            else
                tcmd="socat -u stdio TCP:${REMOTEIP}:${TSST_PORT}${sockopt}"
            fi
        fi
    fi

}

parse_cnf()
{
    local group=$1
    local var=$2
    reval=$(my_print_defaults -c $WSREP_SST_OPT_CONF $group | awk -F= '{if ($1 ~ /_/) { gsub(/_/,"-",$1); print $1"="$2 } else { print $0 }}' | grep -- "--$var=" | cut -d= -f2-)
    if [[ -z $reval ]];then 
        [[ -n $3 ]] && reval=$3
    fi
    echo $reval
}

get_footprint()
{
    pushd $WSREP_SST_OPT_DATA 1>/dev/null
    payload=$(du --block-size=1 -c  **/*.ibd **/*.MYI **/*.MYI ibdata1  | awk 'END { print $1 }')
    if my_print_defaults -c $WSREP_SST_OPT_CONF xtrabackup | grep -q -- "--compress";then 
        # QuickLZ has around 50% compression ratio
        # When compression/compaction used, the progress is only an approximate.
        payload=$(( payload*1/2 ))
    fi
    popd 1>/dev/null
    pcmd+=" -s $payload"
    adjust_progress
}

adjust_progress()
{
    if [[ -n $progress && $progress != '1' ]];then 
        if [[ -e $progress ]];then 
            pcmd+=" 2>>$progress"
        else 
            pcmd+=" 2>$progress"
        fi
    elif [[ -z $progress && -n $rlimit  ]];then 
            # When rlimit is non-zero
            pcmd="pv -q"
    fi 

    if [[ -n $rlimit && "$WSREP_SST_OPT_ROLE"  == "donor" ]];then
        wsrep_log_info "Rate-limiting SST to $rlimit"
        pcmd+=" -L \$rlimit"
    fi
}

read_cnf()
{
    sfmt=$(parse_cnf sst streamfmt "tar")
    tfmt=$(parse_cnf sst transferfmt "socat")
    tcert=$(parse_cnf sst tca "")
    tpem=$(parse_cnf sst tcert "")
    encrypt=$(parse_cnf sst encrypt 0)
    sockopt=$(parse_cnf sst sockopt "")
    progress=$(parse_cnf sst progress "")
    rebuild=$(parse_cnf sst rebuild 0)
    ttime=$(parse_cnf sst time 0)
    incremental=$(parse_cnf sst incremental 0)
    ealgo=$(parse_cnf xtrabackup encrypt "")
    ekey=$(parse_cnf xtrabackup encrypt-key "")
    ekeyfile=$(parse_cnf xtrabackup encrypt-key-file "")

    # Refer to http://www.percona.com/doc/percona-xtradb-cluster/manual/xtrabackup_sst.html 
    if [[ -z $ealgo ]];then
        ealgo=$(parse_cnf sst encrypt-algo "")
        ekey=$(parse_cnf sst encrypt-key "")
        ekeyfile=$(parse_cnf sst encrypt-key-file "")
    fi
    rlimit=$(parse_cnf sst rlimit "")
    uextra=$(parse_cnf sst use_extra 0)
}

get_stream()
{
    if [[ $sfmt == 'xbstream' ]];then 
        wsrep_log_info "Streaming with xbstream"
        if [[ "$WSREP_SST_OPT_ROLE"  == "joiner" ]];then
            strmcmd="xbstream -x"
        else
            strmcmd="xbstream -c \${INFO_FILE} \${IST_FILE}"
        fi
    else
        sfmt="tar"
        wsrep_log_info "Streaming with tar"
        if [[ "$WSREP_SST_OPT_ROLE"  == "joiner" ]];then
            strmcmd="tar xfi - --recursive-unlink -h"
        else
            strmcmd="tar cf - \${INFO_FILE} \${IST_FILE}"
        fi

    fi
}

get_proc()
{
    set +e
    nproc=$(grep -c processor /proc/cpuinfo)
    [[ -z $nproc || $nproc -eq 0 ]] && nproc=1
    set -e
}

sig_joiner_cleanup()
{
    wsrep_log_error "Removing $MAGIC_FILE file due to signal"
    rm -f "$MAGIC_FILE"
}

cleanup_joiner()
{
    # Since this is invoked just after exit NNN
    local estatus=$?
    if [[ $estatus -ne 0 ]];then 
        wsrep_log_error "Cleanup after exit with status:$estatus"
    fi
    if [ "${WSREP_SST_OPT_ROLE}" = "joiner" ];then
        wsrep_log_info "Removing the sst_in_progress file"
        wsrep_cleanup_progress_file
    fi
    if [[ -n $progress && -p $progress ]];then 
        wsrep_log_info "Cleaning up fifo file $progress"
        rm $progress
    fi
}

check_pid()
{
    local pid_file="$1"
    [ -r "$pid_file" ] && ps -p $(cat "$pid_file") >/dev/null 2>&1
}

kill_xtrabackup()
{
#set -x
    local PID=$(cat $XTRABACKUP_PID)
    [ -n "$PID" -a "0" != "$PID" ] && kill $PID && (kill $PID && kill -9 $PID) || :
    rm -f "$XTRABACKUP_PID"
#set +x
}

# waits ~10 seconds for nc to open the port and then reports ready
# (regardless of timeout)
wait_for_nc()
{
    local PORT=$1
    local ADDR=$2
    local MODULE=$3
    for i in $(seq 1 50)
    do
        netstat -nptl 2>/dev/null | grep '/nc\s*$' | awk '{ print $4 }' | \
        sed 's/.*://' | grep \^${PORT}\$ >/dev/null && break
        sleep 0.2
    done
    echo "ready ${ADDR}/${MODULE}"
}

INNOBACKUPEX_BIN=innobackupex
INNOBACKUPEX_ARGS=""
NC_BIN=nc

for TOOL_BIN in INNOBACKUPEX_BIN NC_BIN ; do
  if ! which ${!TOOL_BIN} > /dev/null 2>&1
  then 
     echo "Can't find ${!TOOL_BIN} in the path"
     exit 22 # EINVAL
  fi
done

#ROLE=$1
#ADDR=$2
readonly AUTH=(${WSREP_SST_OPT_AUTH//:/ })
readonly DATA="${WSREP_SST_OPT_DATA}"
#CONF=$5

INFO_FILE="xtrabackup_galera_info"
IST_FILE="xtrabackup_ist"

MAGIC_FILE="${DATA}/${INFO_FILE}"
rm -f "${MAGIC_FILE}"

if [ "$WSREP_SST_OPT_ROLE" = "donor" ]
then

#    UUID=$6
#    SEQNO=$7
#    BYPASS=$8

    NC_PORT=$(echo $WSREP_SST_OPT_ADDR | awk -F '[:/]' '{ print $2 }')
    REMOTEIP=$(echo $WSREP_SST_OPT_ADDR | awk -F ':' '{ print $1 }')

    if [ $WSREP_SST_OPT_BYPASS -eq 0 ]
    then

        TMPDIR=${TMPDIR:-""}
        if [ -z "${TMPDIR}" ]; then
            # try to get it from my.cnf
            TMPDIR=$(grep -E '^\s*tmpdir' $WSREP_SST_OPT_CONF | \
                     awk -F = '{ print $2 }' | sed 's/^\s//g' | sed 's/\s.*//g' )
            # if failed default to /tmp
            [ -z "${TMPDIR}" ] && TMPDIR="/tmp"
        fi

        INNOBACKUPEX_ARGS="--galera-info --tmpdir=${TMPDIR} --stream=tar
                           --defaults-file=${WSREP_SST_OPT_CONF}
                           --socket=${WSREP_SST_OPT_SOCKET}"

        if [ "${AUTH[0]}" != "(null)" ]; then
           INNOBACKUPEX_ARGS="${INNOBACKUPEX_ARGS} --user=${AUTH[0]}"
        fi

        if [ ${#AUTH[*]} -eq 2 ]; then
           INNOBACKUPEX_ARGS="${INNOBACKUPEX_ARGS} --password=${AUTH[1]}"
        fi

        set +e

        ${INNOBACKUPEX_BIN} ${INNOBACKUPEX_ARGS} ${TMPDIR} \
        2> ${DATA}/innobackup.backup.log | \
        ${NC_BIN} ${REMOTEIP} ${NC_PORT}

        RC=( "${PIPESTATUS[@]}" )
        set -e

        if [ ${RC[0]} -ne 0 ]; then
          wsrep_log_error "${INNOBACKUPEX_BIN} finished with error: ${RC[0]}. " \
                          "Check ${DATA}/innobackup.backup.log"
          exit 22
        elif [  ${RC[1]} -ne 0 ]; then
          wsrep_log_error "${NC_BIN} finished with error: ${RC[1]}"
          exit 22
        fi

        # innobackupex implicitly writes PID to fixed location in ${TMPDIR}
        XTRABACKUP_PID="${TMPDIR}/xtrabackup_pid"

        if check_pid "${XTRABACKUP_PID}"
        then
            wsrep_log_error "xtrabackup process is still running. Killing... "
            kill_xtrabackup
            exit 22
        fi

        rm -f "${XTRABACKUP_PID}"

    else # BYPASS
        STATE="${WSREP_SST_OPT_GTID}"
        echo "continue" # now server can resume updating data
        echo "${STATE}" > "${MAGIC_FILE}"
        echo "1" > "${DATA}/${IST_FILE}"
        (cd ${DATA}; tar cf - ${INFO_FILE} ${IST_FILE}) | ${NC_BIN} ${REMOTEIP} ${NC_PORT}
        rm -f ${DATA}/${IST_FILE}
    fi

    echo "done ${WSREP_SST_OPT_GTID}"

elif [ "${WSREP_SST_OPT_ROLE}" = "joiner" ]
then
    MODULE="xtrabackup_sst"

    rm -f ${DATA}/xtrabackup_*

    ADDR=${WSREP_SST_OPT_ADDR}
    NC_PORT=$(echo ${ADDR} | awk -F ':' '{ print $2 }')
    if [ -z "${NC_PORT}" ]
    then
        NC_PORT=${SST_PORT}
        ADDR="$(echo ${ADDR} | awk -F ':' '{ print $1 }'):${NC_PORT}"
    fi

    wait_for_nc ${NC_PORT} ${ADDR} ${MODULE} &

#    trap "exit 32" HUP PIPE
#    trap "exit 3"  INT TERM
    trap cleanup_joiner HUP PIPE INT TERM

    set +e
    ${NC_BIN} -dl ${NC_PORT}  | tar xfi  - -C ${DATA}  1>&2
    RC=( "${PIPESTATUS[@]}" )
    set -e

    wait %% # join wait_for_nc thread

    if [ ${RC[0]} -ne 0 -o ${RC[1]} -ne 0 ];
    then
        wsrep_log_error "Error while getting st data from donor node: " \
                        "${RC[0]}, ${RC[1]}"
        exit 32
    fi

    if [ ! -r "${MAGIC_FILE}" ]
    then
        # this message should cause joiner to abort
        wsrep_log_error "xtrabackup process ended without creating '${MAGIC_FILE}'"
        exit 32
    fi

    if ! ps -p ${WSREP_SST_OPT_PARENT} >/dev/null
    then
        wsrep_log_error "Parent mysqld process (PID:${WSREP_SST_OPT_PARENT}) terminated unexpectedly." >&2
        exit 32
    fi

    if [ ! -r "${IST_FILE}" ]
    then
        rm -f ${DATA}/ib_logfile*
        ${INNOBACKUPEX_BIN} --defaults-file=${WSREP_SST_OPT_CONF} --apply-log \
        --ibbackup=xtrabackup ${DATA} 1>&2 2> ${DATA}/innobackup.prepare.log
        if [ $? -ne 0 ];
        then
            wsrep_log_error "${INNOBACKUPEX_BIN} finished with errors. Check ${DATA}/innobackup.prepare.log" >&2
            exit 22
        fi
    fi

    cat "${MAGIC_FILE}" # output UUID:seqno

else
    wsrep_log_error "Unrecognized role: ${WSREP_SST_OPT_ROLE}"
    exit 22 # EINVAL
fi

exit 0
