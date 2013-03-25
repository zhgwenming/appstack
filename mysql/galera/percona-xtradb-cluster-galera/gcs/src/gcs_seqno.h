/*
 * Copyright (C) 2008 Codership Oy <info@codership.com>
 *
 * $Id: gcs_seqno.h 279 2008-04-06 13:53:58Z alex $
 */
/*
 *  Operations on seqno.
 */

#ifndef _gcs_seqno_h_
#define _gcs_seqno_h_

#include "galerautils.h"
#include "gcs.h"

#define gcs_seqno_le(x) gu_le64(x)
#define gcs_seqno_be(x) gu_be64(x)

#endif /* _gcs_seqno_h_ */
