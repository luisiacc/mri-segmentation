import { useQuery } from 'react-query'

import { fetchPatients } from '../requests/api'

export function useFetchDataPatients() {
  const response = useQuery<any, Error>('fetch-patients', fetchPatients, {
    refetchOnWindowFocus: false,
  })

  return { ...response, data: response?.data?.data || [] }
}
