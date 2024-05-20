import React, { useState } from "react";
import axios from "axios";

const GetEntregado = ({ id, Correo, Destinatario }) => {
  const [entregado, setEntregado] = useState(false);

  const modificarEnvio = async () => {
    try {
      const response = await axios.patch(`http://127.0.0.1:4000/entregarEnvio/${id}/${Correo}/${Destinatario}`, {
        entregado: true
      });

      if (response.status === 200) {
        setEntregado(true);
      } else {
        console.error("Error al modificar el envío:", response.data);
      }
    } catch (error) {
      console.error("Error al modificar el envío:", error);
    }
  };

  return (
    <div>
      {!entregado && (
        <button onClick={modificarEnvio}>Marcar como entregado</button>
      )}
      {entregado && <p>Envío marcado como entregado correctamente.</p>}
    </div>
  );
};

export default GetEntregado;
