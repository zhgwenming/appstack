/*
 * Copyright (C) 2008-2011 Codership Oy <info@codership.com>
 *
 * $Id: gcs_act.h 2383 2011-09-24 11:14:06Z alex $
 */

#ifndef _gcs_act_h_
#define _gcs_act_h_

#include "gcs.h"

struct gcs_act
{
    const void*    buf;
    ssize_t        buf_len;
    gcs_act_type_t type;
};

struct gcs_act_rcvd
{
    struct gcs_act act;
    const void*    repl_buf;    // pointer to local replicated buffer if any
    gcs_seqno_t    id;          // global total order seqno
    int            sender_idx;
};

#endif /* _gcs_act_h_ */
