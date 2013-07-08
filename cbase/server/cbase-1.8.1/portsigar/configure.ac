AC_INIT([sigar_port], 1.0)
AM_INIT_AUTOMAKE
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_FILES([Makefile])
AC_PROG_CC
AC_PROG_LIBTOOL

AC_CHECK_LIB([sigar], [main], [SIGAR_LDFLAGS="${LDFLAGS} -lsigar"], [
  mylibdir=`eval echo ${libdir}`
  AS_IF([test "x${mylibdir}" = "xNONE/lib"],
        [ mylibdir="${prefix}/lib"])
  AS_IF([test "x${mylibdir}" = "xNONE/lib"],
        [ mylibdir="${exec_prefix}/lib"])
  AS_IF([test "x${mylibdir}" = "xNONE/lib"],
        [ mylibdir="${ac_default_prefix}/lib"])
  AC_MSG_NOTICE([will check for libsigar in ${mylibdir}])
  unset ac_cv_lib_sigar_main
  LDFLAGS="$LDFLAGS -L${mylibdir}"
  AC_CHECK_LIB([sigar], [main], [
    SIGAR_LDFLAGS="-L${mylibdir} -lsigar"
  ], [
    AC_MSG_ERROR([need libsigar. Consider passing -L<path> in LDFLAGS])
  ], [-L${mylibdir}])
])

AC_CHECK_HEADER([sigar.h], [], [
  AC_MSG_NOTICE([will check for sigar.h in ${prefix}/include])
  unset ac_cv_header_sigar_h
  ac_func_search_save_CPPFLAGS=$CPPFLAGS
  CPPFLAGS="$CPPFLAGS -I${prefix}/include"
  AC_CHECK_HEADER([sigar.h], [
    SIGAR_CPPFLAGS="-I${prefix}/include"
  ], [
    AC_MSG_ERROR([need sigar.h. Consider passing -I<path> in CPPFLAGS])
  ])
  CPPFLAGS=$ac_func_search_save_CPPFLAGS
])

AC_SUBST(SIGAR_CPPFLAGS)
AC_SUBST(SIGAR_LDFLAGS)

AC_OUTPUT
