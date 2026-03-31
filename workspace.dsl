workspace {
    !docs docs
    !adrs adrs

    model {
        cliente = person "Cliente" "Persona interesada en armar o mejorar su PC."
        admin = person "Administrador" "Gestiona el stock y los precios de componentes."

        ecommerce = softwareSystem "BEGamer Components" "Plataforma para buscar, comparar y comprar hardware." {
            api = container "API Backend" "Maneja la autenticación, autorización, y la lógica de negocio del catálogo." "Python 3.13 slim + FastAPI" {
                tags "API"

                # --- Componentes ---
                catalog_router = component "Catalog Router" "Maneja endpoints de catálogo e imágenes." "FastAPI APIRouter"
                catalog_service = component "Catalog Service" "Orquesta el CRUD de catálogo." "Python Module"
                s3_client = component "S3 Client" "Envoltura para el SDK de AWS." "Boto3"
                catalog_repo = component "Catalog Repository" "Actualiza/lee las tablas de catálogo." "SQLModel"

                
                auth_router = component "Auth Router" "Maneja el login y emite JWT." "FastAPI APIRouter"
                cart_router = component "Cart Router" "Maneja endpoints CRUD del carrito temporal." "FastAPI APIRouter"
                cart_service = component "Cart Service" "Orquesta lógica del carrito y la fusión (merge) de cuentas." "Python Module"
                cart_identifier = component "Cart Identifier" "Extrae la identidad del usuario (Token o X-Guest-Session-ID)." "FastAPI Depends"
                redis_client = component "Redis Client" "Conexión asíncrona a Redis mediante ConnectionPool." "redis.asyncio"


            }

            database = container "Base de Datos" "Almacena usuarios, productos, etc." "PostgreSQL 15-alpine" {
                tags "Database"
            }

            redis = container "Caché y Carrito" "Almacena datos temporales." "Redis 7-alpine" {
                tags "Database"
            }
        }

        # --- Sistemas Externos ---
        webpay = softwareSystem "Pasarela de Pagos (Sandbox)" "Gestiona transacciones." "External System"
        sii = softwareSystem "Servicio Impuestos Internos (Mock)" "Simula validación de boletas." "External System"
        email_system = softwareSystem "Sistema de Correo" "Envía confirmaciones." "External System"
        aws_s3 = softwareSystem "AWS S3" "Almacena imágenes." "External System"
   
        # --- Relaciones Nivel 1 ---
        cliente -> ecommerce "Busca componentes y compra"
        admin -> ecommerce "Gestiona inventario"
        ecommerce -> aws_s3 "Almacena imágenes de productos"
        ecommerce -> webpay "Inicia transacción y valida estado"
        ecommerce -> sii "Solicita folio y timbre electrónico"
        ecommerce -> email_system "Envía correos electrónicos"
        
        # --- Relaciones Nivel 2 ---
        admin -> api "Gestiona Categorías, Marcas, Productos" "HTTPS/JSON"
        cliente -> api "Consulta Productos Disponibles" "HTTPS/JSON"
        api -> database "Lee/Escribe datos" "SQL/SQLModel"
        api -> aws_s3 "Lee/Escribe imágenes" "HTTPS / S3 API"
        api -> redis "Lee/Escribe estado de carritos" "TCP/RESP"

        # --- Relaciones Nivel 3 (Componentes) ---
        admin -> catalog_router "Sube/elimina imagen" "HTTPS/Multipart"
        catalog_router -> s3_client "Envía archivo binario o la url de una imagen existente" "Async"
        catalog_router -> catalog_service "Pasa DTO con nueva URL o id de la imagen" "Async"
        catalog_service -> catalog_repo "Actualiza registro" "Method Call"
        s3_client -> aws_s3 "Sube/elimina objeto" "HTTPS / AWS API"
        catalog_repo -> database "Ejecuta UPDATE/DELETE" "SQLModel"

# --- Flujo 1: Uso normal del carrito (Añadir/Ver/Borrar) ---
        cliente -> cart_router "Añade/modifica items (POST /items, PATCH...)" "HTTPS/JSON"
        cart_router -> cart_identifier "Inyecta dependencia para saber si es Guest o User" "Inyección"
        cart_router -> cart_service "Pasa datos y delega lógica" "Llamada asíncrona"
        cart_service -> redis_client "Calcula TTL y ejecuta comandos (HSET, HGETALL)" "Llamada asíncrona"

        # --- Flujo 2: El Merge---
        cliente -> auth_router "Inicia sesión enviando credenciales y X-Guest-Session-ID" "HTTPS/JSON"
        
        auth_router -> cart_service "Encola tarea en segundo plano (merge_guest_cart...)" "FastAPI BackgroundTasks"
        
        cart_service -> redis_client "Mueve items de la key 'guest' a la key 'user' y borra la vieja" "Llamada asíncrona"

        # El cliente de Redis se conecta al contenedor de Redis real
        redis_client -> redis "Ejecuta transacciones en memoria" "TCP/RESP"
        
    }

    views {
        systemContext ecommerce "DiagramaContexto" {
            include *
            autolayout lr
        }

        container ecommerce "Contenedores" {
            include *
            autolayout lr
        }

        # ESTA VISTA FALTABA: Para ver los componentes dentro de la API
        component api "Componentes" {
            include *
            autolayout lr
            description "Diagrama de componentes de la API Backend (Gestión de Imágenes)"
        }
        
        styles {
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "External System" {
                background #999999
                color #ffffff
            }
            element "API" {
                shape RoundedBox
                background #438dd5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
                background #255fa1
                color #ffffff
            }
        }
    }
}