import { useQuery } from 'react-query'

import { postMRIs } from '../requests/api'

export function useFetchDataMRIs(mrisParams: unknown) {
  const response = useQuery<any, Error>(['fetch-mris', mrisParams], () => postMRIs(mrisParams), {
    refetchOnWindowFocus: false,
    enabled: false,
  })

  return { ...response, data: response?.data?.data || [] }
}
