import * as React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import theme from "./theme";
import Home from "./Pages/Home";
import DayPlanning from "./Pages/DayPlanning";
import SnellDensity from "./Pages/SnellDensity";

export const App = () => (
  <ChakraProvider theme={theme}>
    <Router>
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/day" element={<DayPlanning />} />
        <Route path="/snell" element={<SnellDensity />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  </ChakraProvider>
);
