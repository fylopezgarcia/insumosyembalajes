/*
  Lista de municipios de Colombia para sugerir autocompletado cuando el
  cliente elige "Otra ciudad" en la Tienda. No es el listado oficial exacto
  del DANE (no tenemos acceso a internet para descargarlo) — es una lista
  amplia por departamento hecha desde conocimiento entrenado. Es solo una
  SUGERENCIA: el campo sigue siendo de texto libre, así que si un municipio
  no aparece aquí, el cliente puede escribirlo igual y funciona normal.
*/
(function () {
  var CIUDADES = [
    // Amazonas
    "Leticia", "Puerto Nariño",
    // Antioquia
    "Medellín", "Bello", "Itagüí", "Envigado", "Rionegro", "Apartadó", "Turbo", "Caucasia",
    "Sabaneta", "La Estrella", "Copacabana", "Girardota", "Marinilla", "El Carmen de Viboral",
    "Santa Fe de Antioquia", "Yarumal", "Andes", "Ciudad Bolívar", "Chigorodó", "Necoclí",
    "Puerto Berrío", "Segovia", "Remedios", "Amalfi", "Santa Rosa de Osos", "Don Matías",
    "San Pedro de los Milagros", "Guarne", "El Retiro", "La Ceja", "Carmen de Viboral",
    // Arauca
    "Arauca", "Arauquita", "Saravena", "Tame", "Fortul",
    // Atlántico
    "Barranquilla", "Soledad", "Malambo", "Sabanalarga", "Puerto Colombia", "Baranoa",
    "Galapa", "Sabanagrande", "Santo Tomás", "Palmar de Varela", "Ponedera", "Repelón",
    // Bogotá D.C.
    "Bogotá",
    // Bolívar
    "Cartagena", "Magangué", "Turbaco", "Arjona", "El Carmen de Bolívar", "María la Baja",
    "San Juan Nepomuceno", "Mompóx", "San Pablo", "Simití", "Achí", "Clemencia",
    // Boyacá
    "Tunja", "Duitama", "Sogamoso", "Chiquinquirá", "Puerto Boyacá", "Paipa", "Villa de Leyva",
    "Moniquirá", "Nobsa", "Tibasosa", "Ramiriquí", "Garagoa", "Miraflores", "Aquitania",
    "Samacá", "Ventaquemada", "Guateque", "Soatá",
    // Caldas
    "Manizales", "La Dorada", "Chinchiná", "Villamaría", "Riosucio", "Anserma", "Salamina",
    "Aguadas", "Supía", "Palestina", "Neira", "Manzanares", "Pácora", "Aranzazu", "Filadelfia",
    "Marulanda", "Marmato", "Risaralda (Caldas)", "Viterbo", "Belalcázar",
    // Caquetá
    "Florencia", "San Vicente del Caguán", "Puerto Rico", "El Doncello", "La Montañita",
    "Cartagena del Chairá", "Curillo", "Belén de los Andaquíes",
    // Casanare
    "Yopal", "Aguazul", "Villanueva", "Tauramena", "Monterrey", "Paz de Ariporo", "Trinidad",
    "Orocué", "Hato Corozal",
    // Cauca
    "Popayán", "Santander de Quilichao", "Puerto Tejada", "El Tambo", "Patía", "Piendamó",
    "Corinto", "Miranda", "Timbío", "Cajibío", "Silvia", "Guapi", "Bolívar (Cauca)",
    "Caloto", "Suárez",
    // Cesar
    "Valledupar", "Aguachica", "Codazzi", "La Jagua de Ibirico", "Bosconia", "Curumaní",
    "El Copey", "San Alberto", "San Martín", "Chiriguaná", "La Paz", "Astrea",
    // Chocó
    "Quibdó", "Istmina", "Tadó", "Condoto", "Riosucio (Chocó)", "Acandí", "Bahía Solano",
    "Nuquí", "Bagadó",
    // Córdoba
    "Montería", "Cereté", "Sahagún", "Lorica", "Planeta Rica", "Montelíbano", "Tierralta",
    "Ciénaga de Oro", "San Andrés de Sotavento", "Puerto Libertador", "Ayapel", "Chinú",
    "San Pelayo", "Valencia (Córdoba)",
    // Cundinamarca
    "Soacha", "Facatativá", "Zipaquirá", "Chía", "Mosquera", "Madrid (Cundinamarca)",
    "Funza", "Fusagasugá", "Girardot", "Cajicá", "Cota", "Tocancipá", "Sibaté", "La Calera",
    "Tenjo", "Sopó", "Ubaté", "Ubalá", "Guaduas", "Villeta", "La Mesa", "Anapoima",
    "Silvania", "Cáqueza", "Chocontá",
    // Guainía
    "Inírida",
    // Guaviare
    "San José del Guaviare", "Calamar (Guaviare)", "El Retorno",
    // Huila
    "Neiva", "Pitalito", "Garzón", "La Plata", "Campoalegre", "Palermo (Huila)", "Gigante",
    "Timaná", "Aipe", "Rivera", "San Agustín", "Isnos", "Algeciras", "Yaguará",
    // La Guajira
    "Riohacha", "Maicao", "Uribia", "Manaure", "Fonseca", "San Juan del Cesar", "Villanueva (Guajira)",
    "Barrancas", "Dibulla", "Urumita", "El Molino",
    // Magdalena
    "Santa Marta", "Ciénaga", "Fundación", "Aracataca", "El Banco", "Plato", "Zona Bananera",
    "Pivijay", "Sitionuevo", "Pueblo Viejo", "Ariguaní",
    // Meta
    "Villavicencio", "Acacías", "Granada (Meta)", "San Martín (Meta)", "Puerto López",
    "Puerto Gaitán", "Cumaral", "Restrepo (Meta)", "Guamal", "Castilla la Nueva", "El Dorado (Meta)",
    // Nariño
    "Pasto", "Ipiales", "Tumaco", "Túquerres", "Samaniego", "La Unión (Nariño)", "Sandoná",
    "Barbacoas", "El Charco", "La Cruz (Nariño)", "Cumbal", "Guachucal", "Pupiales",
    // Norte de Santander
    "Cúcuta", "Ocaña", "Pamplona", "Villa del Rosario", "Los Patios", "Tibú", "El Zulia",
    "Chinácota", "Abrego", "Convención", "Sardinata", "Toledo (N. de Santander)",
    // Putumayo
    "Mocoa", "Puerto Asís", "Orito", "Valle del Guamuez", "Sibundoy", "Villagarzón", "Puerto Guzmán",
    // Quindío
    "Armenia", "Calarcá", "Montenegro", "La Tebaida", "Circasia", "Quimbaya", "Filandia",
    "Salento", "Génova (Quindío)", "Buenavista (Quindío)", "Córdoba (Quindío)", "Pijao",
    // Risaralda
    "Pereira", "Dosquebradas", "Santa Rosa de Cabal", "La Virginia", "Marsella", "Belén de Umbría",
    "Apía", "Santuario", "Guática", "Quinchía", "Mistrató", "Pueblo Rico", "Balboa (Risaralda)",
    // San Andrés y Providencia
    "San Andrés", "Providencia",
    // Santander
    "Bucaramanga", "Floridablanca", "Girón", "Piedecuesta", "Barrancabermeja", "San Gil",
    "Socorro", "Barbosa (Santander)", "Málaga", "Vélez", "Puerto Wilches", "Lebrija",
    "Rionegro (Santander)", "Cimitarra", "Sabana de Torres", "Charalá", "Zapatoca",
    "San Vicente de Chucurí", "Confines",
    // Sucre
    "Sincelejo", "Corozal", "Sampués", "San Marcos (Sucre)", "San Onofre", "Tolú",
    "Coveñas", "Sincé", "Galeras", "Ovejas", "Majagual", "Guaranda",
    // Tolima
    "Ibagué", "Espinal", "Melgar", "Honda", "Chaparral", "Líbano", "Mariquita", "Fresno",
    "Guamo", "Purificación", "Flandes", "Lérida", "Armero", "Venadillo", "Ambalema",
    "Ortega", "Rovira", "Cajamarca", "Saldaña",
    // Valle del Cauca
    "Cali", "Palmira", "Buenaventura", "Tuluá", "Cartago", "Buga", "Jamundí", "Yumbo",
    "Candelaria (Valle)", "Florida (Valle)", "Pradera", "Zarzal", "Roldanillo", "La Unión (Valle)",
    "Sevilla", "Caicedonia", "Ginebra", "Guacarí", "El Cerrito", "Restrepo (Valle)",
    "Andalucía (Valle)", "Bugalagrande", "Yotoco", "Vijes", "Dagua", "La Cumbre",
    // Vaupés
    "Mitú",
    // Vichada
    "Puerto Carreño", "La Primavera", "Cumaribo"
  ];

  document.addEventListener("DOMContentLoaded", function () {
    var dl = document.createElement("datalist");
    dl.id = "ciudades-co-list";
    CIUDADES.forEach(function (c) {
      var opt = document.createElement("option");
      opt.value = c;
      dl.appendChild(opt);
    });
    document.body.appendChild(dl);
  });
})();
