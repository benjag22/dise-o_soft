import React from 'react'; 
import { HashRouter as Router, BrowserRouter, Route, Routes } from "react-router-dom";
import Formulario from "./Formulario/Formulario";
import EnviosComponent from './Otros/EnviosComponent ';
import { Page1 } from './pages/page1';
import { IngresoDatosRemitente } from './pages/IngresoDatosRemitente';

function App() {
    return (
      <Router>
        <Routes>
          <Route path='/' element={<Formulario/>}/>
          <Route path='/IngresoDatosRemitente' element={<IngresoDatosRemitente/>}/>
          <Route path='/envio' element={<EnviosComponent/>}/>
        </Routes>
      </Router>
    );
}
export default App;
