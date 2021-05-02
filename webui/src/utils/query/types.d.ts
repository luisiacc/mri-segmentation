import { AxiosRequestConfig, Method } from "axios"

export type AxiosQueryParams = {
  method: Method
  url: string
  config?: AxiosRequestConfig
}

export type Pacients = {
  name: string
}

export type Mri = {
  name: string
}

export type DataType = Pacients | Mri
