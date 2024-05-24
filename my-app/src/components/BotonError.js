import React, { useState, useEffect } from "react";
import { format } from "date-fns";
import { useNavigate } from 'react-router-dom';
import "../Formulario/ButtonStyle.css";

export function BotonError({mensaje=""}) {

    //funciones varias para el jsx
    if (mensaje == "")
        return (<></>);

    return (
            
        <div className="pasar_pagina">
            algo raro
        </div>

    )
}

