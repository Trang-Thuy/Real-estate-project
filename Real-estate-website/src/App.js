import React from 'react';
import "./App.css"
import CssBaseline from '@mui/material/CssBaseline';
import {useRoutes} from "react-router-dom";
import routes from "./app/routes";
import {createTheme, ThemeProvider} from "@mui/material";

function App() {

    const theme = React.useMemo(
        () =>
            createTheme({
                palette: {
                    primary: {
                        main: '#27ae60',
                    }
                },
            }),
        []
    );
    const routing = useRoutes(routes);
    return <ThemeProvider theme={theme}>
        <CssBaseline />
        {routing}
    </ThemeProvider>
}

export default App
