// Copyright (C) 2012 Codership Oy <info@codership.com>

/**
 * @file external Spooky hash implementation to avoid code bloat
 *
 * $Id: gu_spooky.c 2821 2012-06-20 18:42:43Z alex $
 */

#include "gu_spooky.h"

void
gu_spooky128_host (const void* const msg, size_t const len, uint64_t* res)
{
    gu_spooky_inline (msg, len, res);
}
