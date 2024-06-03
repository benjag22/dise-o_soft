import React from 'react'; 
import { HashRouter as Router, BrowserRouter, Route, Routes } from "react-router-dom";
import Home from './pages/Home';
import EnviosComponent from './Otros/EnviosComponent ';
import { IngresoDatosRemitente } from './pages/IngresoDatosRemitente';
import { IngresoDatosDestinatario } from './pages/IngresoDatosDestinatario';
import { DatosEnvio } from './pages/DatosEnvio';
import DetallesEnvio from './Otros/DetallesEnvio'
function App() {
    return (
      <Router>
        <Routes>
          <Route path='/' element={<Home/>}/>
          <Route path='/enviosPorPagar' element={<EnviosComponent/>}/>
          <Route path='/IngresoDatosRemitente' element={<IngresoDatosRemitente/>}/>
          <Route path='/detalle-envio/:id' element={<DetallesEnvio/>}/>
          <Route path='/IngresoDatosDestinatario' element={<IngresoDatosDestinatario/>}/>
          <Route path='/IngresoDatosDeEnvio' element={<DatosEnvio/>}/>
        </Routes>
      </Router>
    );
}
export default App;
