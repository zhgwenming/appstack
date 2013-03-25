/*
 * Copyright (C) 2008 Codership Oy <info@codership.com>
 *
 * $Id: gcs_recv_msg.h 2272 2011-07-28 23:24:41Z alex $
 */

/*!
 * Receiving message context
 */

#ifndef _gcs_recv_msg_h_
#define _gcs_recv_msg_h_

#include "gcs_msg_type.h"

typedef struct gcs_recv_msg
{
    void*          buf;
    long           buf_len;
    long           size;
    long           sender_idx;
    gcs_msg_type_t type;
}
gcs_recv_msg_t;

#endif /* _gcs_recv_msg_h_ */
