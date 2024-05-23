import React from 'react'; 
import { HashRouter as Router, BrowserRouter, Route, Routes } from "react-router-dom";
import Formulario from "./Formulario/Formulario";
import EnviosComponent from './Otros/EnviosComponent ';
import { IngresoDatosRemitente } from './pages/IngresoDatosRemitente';
import { IngresoDatosDestinatario } from './pages/IngresoDatosDestinatario';
import { DatosEnvio } from './pages/DatosEnvio';

function App() {
    return (
      <Router>
        <Routes>
          <Route path='/' element={<Formulario/>}/>
          <Route path='/IngresoDatosRemitente' element={<IngresoDatosRemitente/>}/>
          <Route path='/IngresoDatosDestinatario' element={<IngresoDatosDestinatario/>}/>
          <Route path='/IngresoDatosDeEnvio' element={<DatosEnvio/>}/>

        </Routes>
      </Router>
    );
}
export default App;
