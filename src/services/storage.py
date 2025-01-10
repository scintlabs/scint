class StorageManager:
    def __init__(self, connection_pool):
        super().__init__()
        self.connection_pool = connection_pool

    async def save_struct(self, struct):
        query, params = struct._strategy.build_insert_or_update_query(struct)
        async with self.connection_pool.acquire() as conn:
            await conn.execute(query, *params)

    async def load_struct(self, struct_id: str):
        query = "SELECT * FROM structs WHERE struct_id = $1"
        async with self.connection_pool.acquire() as conn:
            record = await conn.fetchrow(query, struct_id)

        if record:
            strategy = self._pick_strategy_for(record)
            struct = strategy.build_struct_from_record(record)
            return struct

        return None
