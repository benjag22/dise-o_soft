const GetDetalleEnvio = async (envioId) => {
    const response = await fetch(`http://127.0.0.1:4000/detalle_envio/${envioId}`);
    if (!response.ok) {
      throw new Error('error: ');
    }
    const data = await response.json();
    return data;
  };
  
  export default GetDetalleEnvio;
  