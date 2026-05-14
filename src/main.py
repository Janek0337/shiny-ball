import numpy as np
import cv2 as cv
import keyboard
import geometry

def main():
    width = 800
    height = 800

    light_source = geometry.Point(-2, -2, 8, 0.5)
    camera = geometry.Point(0, 0, 10, 0)
    sphere = geometry.sphere(0, 0, 0, 0.8)

    Ia = 0.1
    Ip = 3.0

    materials = {
        "Copper": {
            "ka": np.array([0.0225, 0.0735, 0.19125]),
            "kd": np.array([0.0828, 0.27048, 0.7038]),
            "ks": np.array([0.086014, 0.137622, 0.256777]),
            "n": 12.8
        },
        "Polished Copper": {
            "ka": np.array([0.0275, 0.08825, 0.2295]),
            "kd": np.array([0.066, 0.2118, 0.5508]),
            "ks": np.array([0.0695701, 0.223257, 0.580594]),
            "n": 51.2
        },
        "Gold": {
            "ka": np.array([0.0745, 0.1995, 0.24725]),
            "kd": np.array([0.22648, 0.60648, 0.75164]),
            "ks": np.array([0.366065, 0.555802, 0.628281]),
            "n": 51.2
        },
        "Emerald": {
            "ka": np.array([0.0215, 0.1745, 0.0215]),
            "kd": np.array([0.07568, 0.61424, 0.07568]),
            "ks": np.array([0.633, 0.727811, 0.633]),
            "n": 76.8
        },
        "Chrome": {
            "ka": np.array([0.25, 0.25, 0.25]),
            "kd": np.array([0.4, 0.4, 0.4]),
            "ks": np.array([0.774597, 0.774597, 0.774597]),
            "n": 76.8
        },
        "Black Plastic": {
            "ka": np.array([0.0, 0.0, 0.0]),
            "kd": np.array([0.01, 0.01, 0.01]),
            "ks": np.array([0.5, 0.5, 0.5]),
            "n": 32.0
        }
    }

    mat_names = list(materials.keys())
    current_mat_idx = 0

    while True:
        if keyboard.is_pressed('m'):
            current_mat_idx = (current_mat_idx + 1) % len(mat_names)
        if keyboard.is_pressed('n'):
            current_mat_idx = (current_mat_idx - 1) % len(mat_names)

        mat_name = mat_names[current_mat_idx]
        ka = materials[mat_name]["ka"]
        kd = materials[mat_name]["kd"]
        ks = materials[mat_name]["ks"]
        n = materials[mat_name]["n"]

        img = np.full((height, width, 3), 255, dtype=np.uint8)
        x_vals = np.linspace(-1.0, 1.0, width)
        y_vals = np.linspace(1.0, -1.0, height)
        X_plain, Y_plain = np.meshgrid(x_vals, y_vals)
        R2 = X_plain**2 + Y_plain**2
        is_circle = R2 <= sphere.r**2
        Z_plain = np.zeros_like(X_plain)
        Z_plain[is_circle] = np.sqrt(sphere.r**2 - R2[is_circle])

        # wektor normalny
        Nx = X_plain / sphere.r
        Ny = Y_plain / sphere.r
        Nz = Z_plain / sphere.r

        Nx[~is_circle] = 0; Ny[~is_circle] = 0; Nz[~is_circle] = 0

        # wektor do źródła światła
        Lx = light_source.x - X_plain
        Ly = light_source.y - Y_plain
        Lz = light_source.z - Z_plain

        L_dist = np.sqrt(Lx**2 + Ly**2 + Lz**2)

        Lx[is_circle] /= L_dist[is_circle]
        Ly[is_circle] /= L_dist[is_circle]
        Lz[is_circle] /= L_dist[is_circle]

        NdotL = Nx*Lx + Ny*Ly + Nz*Lz
        dot_clipped = np.clip(NdotL, 0.0, 1.0)

        # wektor do oberwatora
        Vx = camera.x - X_plain
        Vy = camera.y - Y_plain
        Vz = camera.z - Z_plain

        V_dist = np.sqrt(Vx**2 + Vy**2 + Vz**2)
        Vx[is_circle] /= V_dist[is_circle]
        Vy[is_circle] /= V_dist[is_circle]
        Vz[is_circle] /= V_dist[is_circle]

        Rx = 2 * NdotL * Nx - Lx
        Ry = 2 * NdotL * Ny - Ly
        Rz = 2 * NdotL * Nz - Lz

        RdotV = Rx*Vx + Ry*Vy + Rz*Vz
        cosa = np.clip(RdotV, 0.0, 1.0)

        fatt = np.clip(1.0 / (1.0 + 0.05 * L_dist + 0.01 * (L_dist**2)), 0.0, 1.0)

        I_color = np.clip(((Ia * ka) + ((fatt * Ip * dot_clipped)[:, :, np.newaxis] * kd) + (fatt * Ip * (cosa**n))[:, :, np.newaxis] * ks) * 255,
                          0, 255).astype(np.uint8)
        img[is_circle] = I_color[is_circle]

        if keyboard.is_pressed('esc'):
            break
        if keyboard.is_pressed('w'): light_source.move([0, 1, 0])
        if keyboard.is_pressed('s'): light_source.move([0, -1, 0])
        if keyboard.is_pressed('a'): light_source.move([-1, 0, 0])
        if keyboard.is_pressed('d'): light_source.move([1, 0, 0])
        if keyboard.is_pressed('q'): light_source.move([0, 0, -1])
        if keyboard.is_pressed('e'): light_source.move([0, 0, 1])

        cv.putText(
            img=img,
            text=f"Light source at ({light_source.x} {light_source.y} {light_source.z})",
            org=(10, 30),
            fontFace=cv.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(0, 0, 0),
            thickness=1,
            lineType=cv.LINE_AA
        )

        cv.putText(
            img=img,
            text=f"Material: {mat_name}",
            org=(10, 60),
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