// Copyright (C) 2012 Codership Oy <info@codership.com>

/**
 * @file "Clean" abort function to avoid stack and core dumps
 *
 * $Id: gu_abort.h 2984 2013-03-05 10:38:09Z teemu $
 */

#ifndef _gu_abort_h_
#define _gu_abort_h_

#ifdef __cplusplus
extern "C" {
#endif

/* This function is for clean aborts, when we can't gracefully exit otherwise */
extern void gu_abort();

#ifdef __cplusplus
}
#endif

#endif /* _gu_abort_h_ */
