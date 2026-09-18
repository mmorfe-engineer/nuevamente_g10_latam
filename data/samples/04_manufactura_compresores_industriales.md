# Manual de Operación y Mantenimiento Preventivo: Compresores de Tornillo Rotativo Industrial (Serie TX-500)

## 1. Descripción del Sistema y Principio de Operación
El compresor de tornillo rotativo con inyección de aceite es una máquina de desplazamiento positivo diseñada para suministro continuo de aire comprimido a presiones de trabajo entre 7.5 y 13.0 bar. 
La compresión ocurre mediante dos rotores helicoidales macho y hembra acoplados que giran en sentido inverso dentro de una carcasa de hierro fundido de alta resistencia.

## 2. Circuito de Lubricación y Enfriamiento de Aceite
El aceite mineral o sintético cumple cuatro funciones críticas e interconectadas:
1. Lubricación continua de los rodamientos de rodillos cónicos y radiales.
2. Sellado hidrodinámico de los intersticios entre los lóbulos de los rotores para evitar recirculación interna.
3. Disipación térmica directa generada por la compresión adiabática del aire.
4. Protección galvánica contra la corrosión de los componentes internos.

La presión mínima de lubricación debe mantenerse en 2.5 bar durante el ciclo de carga. La temperatura óptima de operación del bloque compresor oscila entre 82°C y 93°C.

## 3. Elementos de Control y Regulación Neumática
- **Válvula de Admisión Proporcional:** Regula el caudal volumétrico de aspiración mediante modulación electro-neumática, pasando automáticamente de estado de carga (100% de apertura) a estado de alivio o vacío cuando la presión de la línea alcanza el punto de corte configurado en el transductor.
- **Válvula de Presión Mínima (MPV):** Retiene una presión interna mínima de 4.5 bar en el depósito separador antes de permitir la salida de aire comprimido hacia la red de distribución, garantizando la inyección continua de aceite por diferencial de presión.
- **Cartucho Separador Aire-Aceite:** Filtro coalescente de microfibra de borosilicato que reduce el arrastre residual de lubricante a menos de 3 partes por millón (PPM) en el aire de salida.

## 4. Protocolo de Mantenimiento Preventivo e Inspecciones Periódicas
- **Cada 500 horas:** Inspección visual de fugas de aceite, verificación de tensión de correas trapezoidales de transmisión y drenaje del condensado del tanque recibidor.
- **Cada 2,000 horas:** Reemplazo obligatorio del elemento filtrante de aire de admisión y sustitución del filtro de aceite lubricante (cartucho roscado spin-on).
- **Cada 4,000 horas o 12 meses:** Análisis químico del lubricante para verificar viscosidad cinemática, índice de acidez (TAN) y reemplazo del cartucho separador aire-aceite.
- **Cada 20,000 horas:** Overhaul integral de la unidad de compresión con reemplazo preventivo de rodamientos de apoyo axial y sellos mecánicos de labio de teflón.

## 5. Sistema de Protección Térmica y Enclavamientos de Seguridad
El controlador digital dispone de una sonda termopar PT100 instalada en la boca de descarga del elemento compresor. Si la temperatura alcanza 100°C, el sistema emite una alarma preventiva en el panel HMI. 
Si la temperatura supera los 105°C, el circuito de paro de emergencia [Emergency Stop Interlock] se activa de forma instantánea, cortando la alimentación de la bobina del contactor principal del motor eléctrico para evitar el gripado de los rotores por dilatación térmica.
