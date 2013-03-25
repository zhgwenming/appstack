/*
 * Copyright (C) 2008 Codership Oy <info@codership.com>
 *
 * $Id: gcs_msg_type.c 477 2008-11-08 22:50:34Z alex $
 */

#include "gcs_msg_type.h"

const char* gcs_msg_type_string[GCS_MSG_MAX] = {
    "ERROR",
    "ACTION",
    "LAST",
    "COMPONENT",
    "STATE_UUID",
    "STATE_MSG",
    "JOIN",
    "SYNC",
    "FLOW",
    "CAUSAL"
};
