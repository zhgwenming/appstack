// Copyright (C) 2011 Codership Oy <info@codership.com>

/**
 * @file Clean abort function
 *
 * $Id: gu_abort.c 2745 2012-03-17 00:00:23Z alex $
 */

#include "gu_abort.h"

#define _GNU_SOURCE

#include "gu_log.h"
#include <sys/resource.h> /* for setrlimit() */
#include <signal.h>       /* for signal()    */
#include <stdlib.h>       /* for abort()     */

#ifdef _GNU_SOURCE
#include <errno.h>  /* for program_invocation_name (GNU extension) */
#endif /* _GNU_SOURCE */

void
gu_abort (void)
{
    /* avoid coredump */
    struct rlimit core_limits = { 0, 0 };
    setrlimit (RLIMIT_CORE, &core_limits);

    /* restore default SIGABRT handler */
    signal (SIGABRT, SIG_DFL);

#ifndef __sun__
    gu_info ("%s: Terminated.", program_invocation_name);
#else
    gu_info ("Program terminated.");
#endif /* _GNU_SOURCE */

    abort();
}

