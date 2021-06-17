import { useQuery } from 'react-query'

import { getMRI } from '../requests/api'

export function useFetchMRI(patient: string) {
  const response = useQuery<any, Error>(['fetch-mris', patient], () => getMRI(patient), {
    refetchOnWindowFocus: false,
    enabled: false,
  })

  return { ...response, data: response?.data?.data || [] }
}
