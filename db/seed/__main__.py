import sys

from sqlalchemy import text
from sqlmodel import Session, func, select

from db.database import engine
from models import User

from .common import new_context
from .locations import seed_locations
from .users import seed_alerts, seed_drivers, seed_users
from .vehicles import seed_devices, seed_services, seed_vehicles
from .trips import seed_trips

# TRUNCATE ... CASCADE también vacía las tablas que dependen de estas
# (conductores, alertas, dispositivos, servicios, viajes, posiciones, incidentes, eventos).
# Los catálogos de códigos no se tocan.
RESET_TABLES = "users, vehicles, known_locations"


def reset_database() -> None:
    answer = input(
        "Esto BORRARÁ usuarios, vehículos, ubicaciones y todo lo relacionado "
        "(viajes, posiciones, incidentes, eventos). Escribe SI para continuar: "
    )
    if answer.strip() != "SI":
        print("Operación cancelada.")
        sys.exit(1)

    with engine.begin() as connection:
        connection.execute(text(f"TRUNCATE TABLE {RESET_TABLES} CASCADE"))


def main() -> None:
    if "--reset" in sys.argv:
        reset_database()

    with Session(engine) as session:
        existing_users = session.exec(select(func.count()).select_from(User)).one()
        if existing_users:
            print(
                "Seed cancelado: la tabla 'users' ya contiene datos. "
                "Usa una base de pruebas vacía o ejecuta con --reset."
            )
            sys.exit(1)

        ctx = new_context()
        seed_users(session, ctx)
        seed_drivers(session, ctx)
        seed_alerts(session, ctx)
        seed_locations(session, ctx)
        seed_vehicles(session, ctx)
        seed_devices(session, ctx)
        seed_services(session, ctx)
        seed_trips(session, ctx)
        session.commit()

        print(
            f"Listo -> users: {len(ctx.users)}, drivers: {len(ctx.drivers)}, "
            f"user_alerts: {len(ctx.alerts)}, known_locations: {len(ctx.locations)}, "
            f"vehicles: {len(ctx.vehicles)}, vehicle_devices: {len(ctx.devices)}, "
            f"vehicle_services: {len(ctx.services)}, trips: {len(ctx.trips)}, "
            f"positions: {len(ctx.positions)}"
        )


if __name__ == "__main__":
    main()