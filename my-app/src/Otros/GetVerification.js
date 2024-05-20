import React, { useState, useEffect } from "react";
const GetVerificacion = ({ id, rut,Correo,Destinatario,}) => {
    const [estadoSolicitud, setEstadoSolicitud] = useState(null);
    const [error, setError] = useState(null);
  
    useEffect(() => {
      const fetchVerificacion = async () => {
        try {
          const response = await fetch(`http://127.0.0.1:4000/verificar_rut/${id}/${rut}`);
          if (!response.ok) {
            throw new Error("Error al verificar");
          }
          const data = await response.json();
          setEstadoSolicitud(data.estado_solicitud);
        } catch (error) {
          setError(error.message);
        }
      };
  
      fetchVerificacion();
    }, [rut]);
  
    if (error) {
      return <div>Error: {error}</div>;
    }
  
    return (
      <div>
        {estadoSolicitud ? (
          <div>
            <p>Estado de la solicitud: "Verificado"</p>
          </div>
        ) : (
          <div>Cargando...</div>
        )}
      </div>
    );
  };
  export default GetVerificacion;