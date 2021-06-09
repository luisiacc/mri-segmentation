import axios from 'axios'

import { API_URL } from '../utils/constants'

export type PatientType = {
  id?: number
  name: string
  sex: string
  age: number
  identity_number: string
  municipality: string
  province: string
}

export const fetchPatients = () => axios.get(`${API_URL}/patients`)

export const addPatient = (patient: PatientType) => axios.post(`${API_URL}/patients`, patient)

export const updatePatient = (patient: PatientType) => axios.post(`${API_URL}/patients`, patient)

export const deletePatient = (id: number) => axios.delete(`${API_URL}/patients/?id=${id}`)

export const postMRIs = (mrisParams: any) => axios.post(`${API_URL}/mris`, mrisParams)
