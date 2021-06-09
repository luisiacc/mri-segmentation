import React from 'react'
import { StrictMode } from 'react'
import ReactDOM from 'react-dom'

import CssBaseline from '@material-ui/core/CssBaseline'
import { ThemeProvider } from '@material-ui/core/styles'
import { QueryClientProvider } from 'react-query'

import App from './App'
import { queryClient } from './utils'
import reportWebVitals from './reportWebVitals'
import { theme } from './utils'

ReactDOM.render(
  <StrictMode>
    <CssBaseline />
    {/* <ThemeProvider theme={theme}> */}
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
    {/* </ThemeProvider> */}
  </StrictMode>,
  document.getElementById('root'),
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
