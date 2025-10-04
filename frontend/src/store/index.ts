import { configureStore } from '@reduxjs/toolkit';
import filtersSlice from './filtersSlice';
import { api } from './api';

export const store = configureStore({
  reducer: {
    filters: filtersSlice,
    api: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
