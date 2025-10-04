import { createSlice } from '@reduxjs/toolkit';

interface FiltersState {
  search: string;
  dateFrom?: string;
  dateTo?: string;
  strana?: string;
}

const initialState: FiltersState = {
  search: '',
};

export const filtersSlice = createSlice({
  name: 'filters',
  initialState,
  reducers: {
    setSearch: (state, action) => {
      state.search = action.payload;
    },
    setDateRange: (state, action) => {
      state.dateFrom = action.payload.from;
      state.dateTo = action.payload.to;
    },
    setStrana: (state, action) => {
      state.strana = action.payload;
    },
  },
});

export const { setSearch, setDateRange, setStrana } = filtersSlice.actions;
export default filtersSlice.reducer;
