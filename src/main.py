import numpy as np
import cv2 as cv
import keyboard
import geometry

def main():
    width = 1500
    height = 700
    resolution = width / height

    light_source = geometry.Point(-2, -2, 8, 0.5)
    camera = geometry.Point(0, 0, 10, 0)
    sphere = geometry.sphere(0, 0, 0, 0.8)

    Ia = 0.1
    Ip = 3.0
    ka = 0.19125
    kd = 0.7038
    ks = 0.256777
    n = 12.8

    while True:
        img = np.full((height, width, 3), 255, dtype=np.uint8)
        x_vals = np.linspace(-1.0 * resolution, 1.0 * resolution, width)
        y_vals = np.linspace(-1.0, 1.0, height)
        X_plain, Y_plain = np.meshgrid(x_vals, y_vals)
        R2 = X_plain**2 + Y_plain**2
        is_circle = R2 <= sphere.r**2
        Z_plain = np.zeros_like(X_plain)
        Z_plain[is_circle] = np.sqrt(sphere.r**2 - R2[is_circle])

        Nx = X_plain / sphere.r
        Ny = Y_plain / sphere.r
        Nz = Z_plain / sphere.r

        Nx[~is_circle] = 0
        Ny[~is_circle] = 0
        Nz[~is_circle] = 0

        Lx = light_source.x - X_plain
        Ly = light_source.y - Y_plain
        Lz = light_source.z - Z_plain

        L_dist = np.sqrt(Lx**2 + Ly**2 + Lz**2)

        Lx[is_circle] = Lx[is_circle] / L_dist[is_circle]
        Ly[is_circle] = Ly[is_circle] / L_dist[is_circle]
        Lz[is_circle] = Lz[is_circle] / L_dist[is_circle]

        Lx[~is_circle] = 0
        Ly[~is_circle] = 0
        Lz[~is_circle] = 0

        dot_product = Nx*Lx + Ny*Ly + Nz*Lz
        dot_clipped = np.clip(dot_product, 0.0, 1.0)

        Vx = camera.x - X_plain
        Vy = camera.y - Y_plain
        Vz = camera.z - Z_plain

        V_dist = np.sqrt(Vx**2 + Vy**2 + Vz**2)
        Vx[is_circle] = Vx[is_circle] / V_dist[is_circle]
        Vy[is_circle] = Vy[is_circle] / V_dist[is_circle]
        Vz[is_circle] = Vz[is_circle] / V_dist[is_circle]

        Vx[~is_circle] = 0
        Vy[~is_circle] = 0
        Vz[~is_circle] = 0

        Rx = 2 * dot_product * Nx - Lx
        Ry = 2 * dot_product * Ny - Ly
        Rz = 2 * dot_product * Nz - Lz

        R_dot_V = (Rx * Vx) + (Ry * Vy) + (Rz * Vz)

        cosa = np.clip(R_dot_V, 0.0, 1.0)

        Kc = 1.0
        Kl = 0.05
        Kq = 0.01

        fatt = 1.0 / (Kc + Kl * L_dist + Kq * (L_dist**2))
        fatt = np.clip(fatt, 0.0, 1.0)

        amb_diff = Ia * ka + fatt * Ip * kd * dot_clipped
        spec = fatt * Ip * ks * (cosa**n)

        img[is_circle, 0] = np.clip(amb_diff[is_circle] * 51  + spec[is_circle] * 255, 0, 255).astype(np.uint8)
        img[is_circle, 1] = np.clip(amb_diff[is_circle] * 115 + spec[is_circle] * 255, 0, 255).astype(np.uint8)
        img[is_circle, 2] = np.clip(amb_diff[is_circle] * 184 + spec[is_circle] * 255, 0, 255).astype(np.uint8)


        if keyboard.is_pressed('esc'):
            break
        if keyboard.is_pressed('w'):
            light_source.move([0, -1, 0])
        if keyboard.is_pressed('s'):
            light_source.move([0, 1, 0])
        if keyboard.is_pressed('a'):
            light_source.move([-1, 0, 0])
        if keyboard.is_pressed('d'):
            light_source.move([1, 0, 0])
        if keyboard.is_pressed('q'):
            light_source.move([0, 0, -1])
        if keyboard.is_pressed('e'):
            light_source.move([0, 0, 1])

        cv.putText(
            img=img,
            text=f"Light source at ({light_source.x:.2f} {light_source.y:.2f}, {light_source.z:.2f})",
            org=(10, 30),
            fontFace=cv.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(0, 0, 0),
            thickness=1,
            lineType=cv.LINE_AA
        )

        cv.imshow("Usmiechnij sie, jestes w ukrytej kamerze", img)
        if cv.waitKey(16) & 0xFF == 27:
            break

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()