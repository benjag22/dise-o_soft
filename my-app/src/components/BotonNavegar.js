import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import "../Formulario/ButtonStyle.css";

export function BotonNavegar({paginaAntes="/"},{botonSiguienteTexto="Siguiente"}) {

    const navigate = useNavigate();
    //funciones varias para el jsx
    const volverAtras = () => {
        navigate(paginaAntes);
    }
    return (
            
        <div className="pasar_pagina">
            <button onClick={volverAtras} className="buttons" value="Registrar">
                Volver
            </button>
            <button type="submit" className="buttons" value="Registrar">
            {botonSiguienteTexto}
            </button>
        </div>

    )
}

