/* -*- Mode: C++; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*- */
#ifndef KVSTORE_HH
#define KVSTORE_HH 1

#include <map>
#include <string>
#include <utility>

#include <cstring>

#include "stats.hh"
#include "item.hh"
#include "queueditem.hh"

/**
 * Result of database mutation operations.
 *
 * This is a pair where .first is the number of rows affected, and
 * .second is the ID that was generated (if any).  .second will be 0
 * on updates (not generating an ID).
 *
 * .first will be -1 if there was an error performing the update.
 *
 * .first will be 0 if the update did not error, but did not occur.
 * This would generally be considered a fatal condition (in practice,
 * it requires you to be firing an update at a missing rowid).
 */
typedef std::pair<int, int64_t> mutation_result;

struct vbucket_state {
    std::string state;
    uint64_t checkpointId;
};

/**
 * Type of vbucket map.
 *
 * key.first is the vbucket identifier.
 * key.second is the vbucket version
 * value is a pair of string representation of the vbucket state and
 * its latest checkpoint Id persisted.
 */
typedef std::map<std::pair<uint16_t, uint16_t>, vbucket_state> vbucket_map_t;

/**
 * Properites of the storage layer.
 *
 * If concurrent filesystem access is possible, maxConcurrency() will
 * be greater than one.  One will need to determine whether more than
 * one writer is possible as well as whether more than one reader is
 * possible.
 */
class StorageProperties {
public:

    StorageProperties(size_t c, size_t r, size_t w, bool evb, bool evd)
        : maxc(c), maxr(r), maxw(w), efficientVBDump(evb),
          efficientVBDeletion(evd) {}

    //! The maximum number of active queries.
    size_t maxConcurrency()   const { return maxc; }
    //! Maximum number of active read-only connections.
    size_t maxReaders()       const { return maxr; }
    //! Maximum number of active connections for read and write.
    size_t maxWriters()       const { return maxw; }
    //! True if we can efficiently dump a single vbucket.
    bool hasEfficientVBDump() const { return efficientVBDump; }
    //! True if we can efficiently delete a vbucket all at once.
    bool hasEfficientVBDeletion() const { return efficientVBDeletion; }

private:
    size_t maxc;
    size_t maxr;
    size_t maxw;
    bool efficientVBDump;
    bool efficientVBDeletion;
};

/**
 * Database strategy
 */
enum db_type {
    single_db,           //!< single database strategy
    multi_db,            //!< multi-database strategy
    single_mt_db,        //!< single database, multi-table strategy
    multi_mt_db,         //!< multi-database, multi-table strategy
    multi_mt_vb_db       //!< multi-db, multi-table strategy sharded by vbucket
};

/**
 * Configuration parameters to be passed to KVStore::create
 */
class KVStoreConfig {
public:
    KVStoreConfig(const char *l,
                  const char *sp,
                  const char *i,
                  const char *p,
                  size_t nv,
                  size_t sh) : location(l), shardPattern(sp),
                               initFile(i), postInitFile(p),
                               numVBuckets(nv),
                               shards(sh) {}

    const char   *location;
    const char   *shardPattern;
    const char   *initFile;
    const char   *postInitFile;
    const size_t  numVBuckets;
    const size_t  shards;
};

/**
 * Base class representing kvstore operations.
 */
class KVStore {
public:

    /**
     * Create a KVStore with the given properties.
     *
     * @param type the type of DB to set up
     * @param stats the server stats
     * @param conf type-specific parameters
     */
    static KVStore *create(db_type type,
                           EPStats &stats,
                           const KVStoreConfig &conf);

    /**
     * Get the name of a db type.
     */
    static const char* typeToString(enum db_type type);

    /**
     * Get the type for a given name.
     *
     * @param name the name to parse
     * @param typeOut a reference to a type to fill
     *
     * @return true if we were able to parse the type
     */
    static bool stringToType(const char *name,
                             enum db_type &typeOut);

    virtual ~KVStore() {}

    /**
     * Allow the kvstore to add extra statistics information
     * back to the client
     * @param prefix prefix to use for the stats
     * @param add_stat the callback function to add statistics
     * @param c the cookie to pass to the callback function
     */
    virtual void addStats(const std::string &prefix, ADD_STAT add_stat, const void *c) {
        (void)prefix;
        (void)add_stat;
        (void)c;
    }

    /**
     * Show kvstore specific timing stats.
     *
     * @param prefix prefix to use for the stats
     * @param add_stat the callback function to add statistics
     * @param c the cookie to pass to the callback function
     */
    virtual void addTimingStats(const std::string &, ADD_STAT, const void *) {
    }

    /**
     * Reset the store to a clean state.
     */
    virtual void reset() = 0;

    /**
     * Begin a transaction (if not already in one).
     *
     * @return false if we cannot begin a transaction
     */
    virtual bool begin() = 0;

    /**
     * Commit a transaction (unless not currently in one).
     *
     * @return false if the commit fails
     */
    virtual bool commit() = 0;

    /**
     * Rollback the current transaction.
     */
    virtual void rollback() = 0;

    /**
     * Get the properties of the underlying storage.
     */
    virtual StorageProperties getStorageProperties() = 0;

    /**
     * Set an item into the kv store.
     */
    virtual void set(const Item &item, uint16_t vb_version,
                     Callback<mutation_result> &cb) = 0;
    /**
     * Set the meta fields of a key in the kv store
     */
    virtual void setMeta(const Item &item, uint16_t vb_version,
                         Callback<mutation_result> &cb) = 0;

    /**
     * Get an item from the kv store.
     */
    virtual void get(const std::string &key, uint64_t rowid,
                     uint16_t vb, uint16_t vbver,
                     Callback<GetValue> &cb) = 0;

    /**
     * Delete an item from the kv store.
     */
    virtual void del(const std::string &key, uint64_t rowid,
                     uint16_t vb, uint16_t vbver,
                     Callback<int> &cb) = 0;

    /**
     * Bulk delete some versioned records from a vbucket.
     */
    virtual bool delVBucket(uint16_t vbucket, uint16_t vb_version) = 0;

    /**
     * Bulk delete some versioned records from a vbucket.
     */
    virtual bool delVBucket(uint16_t vbucket, uint16_t vb_version,
                            std::pair<int64_t, int64_t> row_range) = 0;

    /**
     * Get a list of all persisted vbuckets (with their versions and states).
     */
    virtual vbucket_map_t listPersistedVbuckets(void) = 0;

    /**
     * Persist a snapshot of a collection of stats.
     */
    virtual bool snapshotStats(const std::map<std::string, std::string> &m) = 0;

    /**
     * Snapshot vbucket states.
     */
    virtual bool snapshotVBuckets(const vbucket_map_t &m) = 0;

    /**
     * Pass all stored data through the given callback.
     */
    virtual void dump(Callback<GetValue> &cb) = 0;

    /**
     * Pass all stored data for the given vbucket through the given
     * callback.
     */
    virtual void dump(uint16_t vbid, Callback<GetValue> &cb) = 0;

    /**
     * Get the number of data shards in this kvstore.
     */
    virtual size_t getNumShards() = 0;

    /**
     * get the shard ID for the given queued item.
     */
    virtual size_t getShardId(const QueuedItem &i) = 0;

    /**
     * Before persisting a batch of data, do stuf to them that might
     * improve performance at the IO layer.
     */
    virtual void optimizeWrites(std::vector<queued_item> &items) = 0;

    /**
     * Remove invalid vbuckets from the underlying storage engine.
     * @param destroyOnlyOne True if this run should remove only one invalid vbucket.
     * This can be set to true if we want to delete all invalid vbuckets over the time.
     */
    virtual void destroyInvalidVBuckets(bool destroyOnlyOne = false) = 0;

};

#endif // KVSTORE_HH
