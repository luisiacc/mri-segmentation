import { createMuiTheme, ThemeOptions } from "@material-ui/core/styles"

//TODO: Create custom mui theme
export const theme = (options: ThemeOptions) => {
  return createMuiTheme({
    ...options,
  })
}
