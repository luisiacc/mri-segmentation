import { useQuery } from 'react-query'

import { getPatients } from '../requests/api'

export function useFetchPatients() {
  const response = useQuery<any, Error>('fetch-patients', getPatients, {
    refetchOnWindowFocus: false,
  })

  return { ...response, data: response?.data?.data || [] }
}
