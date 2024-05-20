
export const GetEnvios = async () => {
  try {
    const res = await fetch("http://127.0.0.1:4000/envios/por_pagar");
    if (!res.ok) {
      throw new Error("Error al obtener los envíos");
    }
    const dataJson = await res.json();
    return dataJson;
  } catch (error) {
    console.error("Error en la solicitud de envíos:", error);
    return []; 
  }
};
