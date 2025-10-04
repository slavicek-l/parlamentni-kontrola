import { useSearchParams } from 'react-router-dom';
import { useMemo } from 'react';

export function useQueryParams() {
  const [searchParams, setSearchParams] = useSearchParams();

  const params = useMemo(() => {
    return Object.fromEntries(searchParams.entries());
  }, [searchParams]);

  const updateParams = (newParams: Record<string, string>) => {
    setSearchParams({ ...params, ...newParams });
  };

  return { params, updateParams };
}
