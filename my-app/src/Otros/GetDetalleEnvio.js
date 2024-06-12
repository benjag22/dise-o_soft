const GetDetalleEnvio = async (envioId) => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/envios/${envioId}`);
    if (!response.ok) {
      throw new Error('Error al obtener los detalles del envío');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error en la solicitud de detalles del envío:', error);
    return null;
  }
};

export default GetDetalleEnvio;
