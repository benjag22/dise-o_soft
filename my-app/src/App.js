import React from 'react'; 
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Formulario from "./Formulario/Formulario";
import EnviosComponent from './Otros/EnviosComponent ';

function App() {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Formulario/>} />
          <Route path="/envios" element={<EnviosComponent/>} />
        </Routes>
      </BrowserRouter>
    );
}
export default App;
