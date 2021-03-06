/* -*- Mode: C++; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*- */

#include "config.h"
#include <iostream>
#include <cstdlib>
#include <string>
#include <map>

#include "common.hh"
#include "statsnap.hh"
#include "ep_engine.h"

extern "C" {
    static void add_stat(const char *key, const uint16_t klen,
                         const char *val, const uint32_t vlen,
                         const void *cookie) {
        assert(cookie);
        void *cokie = const_cast<void *>(cookie);
        StatSnap *ssnap = static_cast<StatSnap *>(cokie);

        ObjectRegistry::onSwitchThread(ssnap->getEngine());
        std::string k(key, klen);
        std::string v(val, vlen);
        ssnap->getMap()[k] = v;
    }
}

bool StatSnap::getStats(const char *s) {
    map.clear();
    return engine->getStats(this, s, s ? strlen(s) : 0,
                            add_stat) == ENGINE_SUCCESS;
}

bool StatSnap::callback(Dispatcher &d, TaskId t) {
    if (getStats()) {
        engine->getEpStore()->getRWUnderlying()->snapshotStats(map);
    }
    d.snooze(t, STATSNAP_FREQ);
    return true;
}
