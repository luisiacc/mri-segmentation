import axios from "axios"
import { QueryClient, QueryFunctionContext, QueryKey } from "react-query/core"

import { AxiosQueryParams, DataType } from "./types"
import { API_URL } from "../constants"

export const axiosQuery = ({ method, url, config = {} }: AxiosQueryParams) => {
  const source = axios.CancelToken.source()

  const promise = axios({
    method,
    url,
    cancelToken: source.token,
    ...config,
  })

  return promise
}

axiosQuery.get = (url: string) => axiosQuery({ method: "get", url: url })

axiosQuery.post = (url: string, data: DataType) =>
  axiosQuery({ method: "post", url: url, config: { data } })

axiosQuery.put = (url: string, data: DataType) =>
  axiosQuery({ method: "put", url: url, config: { data } })

axiosQuery.patch = (url: string, data: DataType) =>
  axiosQuery({ method: "patch", url: url, config: { data } })

axiosQuery.delete = (url: string) => axiosQuery({ method: "delete", url: url })

const defaultQueryFn = async ({
  queryKey,
}: QueryFunctionContext<QueryKey, any>) => {
  const { data } = await axiosQuery.get(API_URL + queryKey[0])
  return data
}

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: defaultQueryFn,
    },
  },
})
