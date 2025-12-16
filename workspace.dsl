workspace {

    model {
        # --- Actores ---
        cliente = person "Cliente" "Persona interesada en armar o mejorar su PC."
        admin = person "Administrador" "Gestiona el stock y los precios de componentes."

        # --- Tu Sistema ---
        ecommerce = softwareSystem "BEGamer Components" "Plataforma para buscar, comparar y comprar hardware." {
            # Le dice a Structurizr que busque la documentación dentro de estas carpetas
            !docs docs
            !adrs adrs
            api = container "API Backend" "Maneja la autenticación (Login) y lógica de negocio." "Python 3.11 + FastAPI" {
                tags "API"
            }

            database = container "Base de Datos" "Almacena usuarios, roles y hashes de contraseñas." "PostgreSQL 16" {
                tags "Database"
            }
        }

        # --- Sistemas Externos ---
        webpay = softwareSystem "Pasarela de Pagos (Sandbox)" "Gestiona transacciones bancarias en ambiente de pruebas." "External System"
        
        sii = softwareSystem "Servicio Impuestos Internos (Mock)" "Simula la validación y emisión de boletas para fines académicos." "External System"
        email_system = softwareSystem "Sistema de Correo" "Envía confirmaciones de órdenes y recuperación de claves." "External System"
   
        # --- Relaciones ---
        cliente -> ecommerce "Busca componentes y compra"
        admin -> ecommerce "Gestiona inventario"
        
        ecommerce -> webpay "Inicia transacción y valida estado"
        ecommerce -> sii "Solicita folio y timbre electrónico (Simulado)"
        ecommerce -> email_system "Envía correos electrónicos a clientes"
        # 1. El Admin intenta entrar
        admin -> api "Envía credenciales (POST /auth/login)" "HTTPS/JSON"
        
        # 2. La API verifica quién es
        api -> database "Selecciona usuario y hash de contraseña" "SQL/SQLAlchemy"


    }

    views {
        systemContext ecommerce "DiagramaContexto" {
            include *
            autolayout lr
            title "Diagrama de Contexto - Venta de PC (Entorno Académico)"
        }
        # Vista Nivel 2 (Contenedores)
        container ecommerce "Contenedores" {
            include *
            autolayout lr
            title "Nivel 2: Contenedores (Foco: Autenticación)"
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
            # Estilo para sistemas externos reales o simulados
            element "External System" {
                background #999999
                color #ffffff
            }
            # Estilo visual para diferenciar API de Base de Datos
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