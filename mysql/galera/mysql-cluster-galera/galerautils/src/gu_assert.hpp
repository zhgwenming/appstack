// Copyright (C) 2009 Codership Oy <info@codership.com>

/**
 * @file Assert macro definition
 *
 * $Id: gu_assert.hpp 2984 2013-03-05 10:38:09Z teemu $
 */

#ifndef _gu_assert_hpp_
#define _gu_assert_hpp_

#ifndef DEBUG_ASSERT
#include <cassert>
#else

#include <unistd.h>
#undef assert
#include "gu_logger.hpp"

/** Assert that sleeps instead of aborting the program, saving it for gdb */
#define assert(expr)                                                    \
    if (!(expr)) {                                                      \
        log_fatal << "Assertion (" << __STRING(expr) << ") failed";     \
        while(1) sleep(1);                                              \
    }

#endif /* DEBUG_ASSERT */

#endif /* _gu_assert_hpp_ */
