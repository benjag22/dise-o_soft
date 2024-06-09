import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "./BuscarEnvio.css"

function BuscarEnvio() {
  const [envioId, setEnvioId] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setEnvioId(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const parsedId = parseInt(envioId, 10);
    if (Number.isInteger(parsedId) && parsedId > 0) {
      setError('');
      navigate(`/detalle-envio/${parsedId}`);
    } else {
      setError('Ingrese un id valido');
    }
  };
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          id = "buscaEnvioInput"
          type="text"
          value={envioId}
          onChange={handleInputChange}
          placeholder="Ingrese el ID del envío"
        />
        <button type="submit">Buscar Envío</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default BuscarEnvio;
