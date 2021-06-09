import { Button } from '@material-ui/core'
import React from 'react'
import { QueryClient, QueryClientProvider } from 'react-query'

import { useFetchDataPatients, useFetchDataMRIs } from './hooks'

export type PatientType = {
  id?: number
  name: string
  sex: string
  age: number
  identity_number: string
  municipality: string
  province: string
}

export type MRIsParams = {
  file: File
  patient: PatientType
}

const queryClient = new QueryClient()

const App = () => {
  return (
    <div>
      <ExamplePatientApi />
      <ExampleMRIsApi />
    </div>
  )
}

function ExamplePatientApi() {
  const { isLoading, error, data } = useFetchDataPatients()
  console.log(data)

  if (isLoading) return <p>Loading... </p>

  if (error) return <p>{'An error has occurred: ' + error.message}</p>

  return data.map((patient: PatientType) => (
    <div key={patient?.id}>
      <h1>{patient?.name}</h1>
      <p>{patient?.sex}</p>
      <p>{patient?.age}</p>
      <p>{patient?.identity_number}</p>
      <p>{patient?.municipality}</p>
      <p>{patient?.province}</p>
    </div>
  ))
}

function ExampleMRIsApi() {
  const { isLoading, error, data } = useFetchDataMRIs({ file: '', patient: '' })
  console.log(data)

  if (isLoading) return <p>Loading... </p>

  if (error) return <p>{'An error has occurred: ' + error.message}</p>

  return (
    <Button variant="contained" component="label">
      Upload File
      <input type="file" hidden />
    </Button>
  )
}

export default App
