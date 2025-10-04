import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const API_BASE = import.meta.env.VITE_API_BASE || '/api/v1';

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: API_BASE }),
  endpoints: (builder) => ({
    getPoslanci: builder.query({
      query: (params = {}) => ({
        url: '/poslanci',
        params,
      }),
    }),
    getHlasovani: builder.query({
      query: (params = {}) => ({
        url: '/hlasovani',
        params,
      }),
    }),
  }),
});

export const { useGetPoslanciQuery, useGetHlasovaniQuery } = api;
