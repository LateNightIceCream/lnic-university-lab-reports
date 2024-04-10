import matplotlib.pyplot as plt
import numpy as np


class AntennaArray:
    def __init__(self, lam):
        self.pos = self.get_geometry()
        self.lam = lam

    def get_geometry(self):
        """
        should return the array of complex positions
        overridden by child classes
        """
        return np.zeros(1)

    def get_array_factor_dcos(self, dcosx, dcosy, target_theta, target_phi):
        """
        calculates the array factor for a specific position
        (directional cosines)
        """
        steering_weights = self.get_steering_weights_for_target(target_theta, target_phi)

        xn = self.pos.real
        yn = self.pos.imag

        AF = np.sum(steering_weights * np.exp(-1j*2*np.pi/self.lam * (xn * dcosx + yn * dcosy)))

        return AF

    def get_array_factor(self, theta, phi, target_theta, target_phi):
        """
        calculates the array factor for a specific position (set of angles)
        TODO: normalize this. e.g. theta=0, phi=0 leads to AF=9 (3x3) which
        skews the power
        """
        steering_weights = self.get_steering_weights_for_target(target_theta, target_phi)

        xn = self.pos.real
        yn = self.pos.imag

        AF = np.sum(steering_weights * np.exp(-1j*2*np.pi/self.lam * np.sin(theta) * (xn * np.cos(phi) + yn * np.sin(phi))))

        return AF

    def get_steering_weights_for_target(self, target_theta, target_phi):
        """
        calculates weights (phases) based on target location
        (phased weights)
        """

        xn = self.pos.real
        yn = self.pos.imag

        angle = 2*np.pi / self.lam * np.sin(target_theta) * (xn * np.cos(target_phi) + yn * np.sin(target_phi))

        return np.exp(1j*angle)


class SquareArray(AntennaArray):
    def __init__(self, lam, size, spacing):
        self.size = size
        self.spacing = spacing
        super().__init__(lam)

    def get_geometry(self):
        nx, ny = self.size
        x = np.linspace(0, 1, nx)
        y = np.linspace(0, 1, ny)
        xv, yv = np.meshgrid(x, y)

        # define complex number and scale
        pos = self.spacing * ((nx-1) * xv + 1j * (ny-1) * yv)
        # center around zero
        pos = pos - ((np.max(pos.real) + 1j*np.max(pos.imag))) / 2

        return pos


class EquilateralArray(AntennaArray):
    def __init__(self, lam, size, spacing):
        self.size = size
        self.spacing = spacing
        super().__init__(lam)

    def get_geometry(self):
        nx, ny = self.size
        x = np.linspace(0, 1, nx)
        y = np.linspace(0, 1, ny)
        xv, yv = np.meshgrid(x, y)

        x_shift = np.zeros(self.size)
        # modify every second row
        x_shift[1::2,:] = -self.spacing / 2

        # define complex number and scale
        pos = self.spacing * ((nx-1) * xv + 1j * (ny-1) * yv * np.sqrt(3)/2)
        pos.real = pos.real - x_shift
        # center around zero
        pos = pos - ((np.max(pos.real) + 1j*np.max(pos.imag))) / 2

        return pos


def plot_phase_numbers(array, target_theta, target_phi, scale=1):
    weights = array.get_steering_weights_for_target(
        np.deg2rad(target_theta),
        np.deg2rad(target_phi))
    equilat_phases = np.rad2deg(np.angle(weights)).flatten()
    text_offs = 0.02
    for i, pos in enumerate((array.pos / scale).flatten()):
        plt.text(pos.real + text_offs, pos.imag + text_offs,
                 "%.1f°" % equilat_phases[i],
                 color="gray",
                 size=20)


def main():

    f = 100e6
    c = 3e8
    lam = c / f

    target_phi = 0
    target_theta = 60
    target_azm = np.mod(90 - target_phi, 360)

    spacing = 0.5 * lam

    square_array = SquareArray(lam, (5, 5), spacing)
    equilat_array = EquilateralArray(lam, (5, 5), spacing)

    dcx = np.linspace(-1, 1, 100)
    dcy = np.linspace(-1, 1, 100)

    # ugly but does the job
    afs_square = np.zeros([100, 100])
    afs_equilat = np.zeros([100, 100])
    for i, dx in enumerate(dcx):
        for k, dy in enumerate(dcy):
            af1 = square_array.get_array_factor_dcos(dx, dy,
                                                     np.deg2rad(target_theta),
                                                     np.deg2rad(target_azm))
            af2 = equilat_array.get_array_factor_dcos(dx, dy,
                                                      np.deg2rad(target_theta),
                                                      np.deg2rad(target_azm))
            afs_square[i, k] = np.abs(af1)
            afs_equilat[i, k] = np.abs(af2)

    afs_square_pow = 20*np.log10(afs_square)
    afs_equilat_pow = 20*np.log10(afs_equilat)


    # --------------------------------------------------------------------------
    # Plotting
    # --------------------------------------------------------------------------

    # does not work for some reason
    # dist = np.sqrt(dcx**2 + dcy**2)
    # afs_pow[dist < 1] = np.NAN

    # radiation pattern color plot
    plt.figure()
    plt.suptitle("Square %dx%d Array Factor"
                 % (square_array.size))
    plt.title("$d=%.2f\,\\lambda$, $\\theta_d=%.2f$°,$\\phi_d=%.2f$°"
              % (spacing / lam, target_theta, target_phi))
    plt.axis('equal')
    plt.pcolor(dcx, dcy, afs_square_pow, cmap='jet')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel("$20\\log_{10}{(AF)}$")
    plt.clim(np.max(afs_square_pow)-20, np.max(afs_square_pow))
    plt.xlabel("$\\sin{\\theta}\\cos{\\phi}$")
    plt.ylabel("$\\sin{\\theta}\\sin{\\phi}$")
    plt.savefig("outputs/square-%.2f-lambda-%.2f-theta-%.2f-phi-radpat.pdf"
                % (spacing/lam, target_theta, target_phi))

    plt.figure()
    plt.suptitle("Equilateral %d-Antenna Array Factor"
                 % (np.prod(square_array.size)))
    plt.title("$d=%.2f\,\\lambda$, $\\theta_d=%.2f$°,$\\phi_d=%.2f$°"
              % (spacing / lam, target_theta, target_phi))
    plt.axis('equal')
    plt.pcolor(dcx, dcy, afs_equilat_pow, cmap='jet')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel("$20\\log_{10}{(AF)}$")
    plt.clim(np.max(afs_equilat_pow)-20, np.max(afs_equilat_pow))
    plt.xlabel("$\\sin{\\theta}\\cos{\\phi}$")
    plt.ylabel("$\\sin{\\theta}\\sin{\\phi}$")
    plt.savefig("outputs/equilat-%.2f-lambda-%.2f-theta-%.2f-phi-radpat.pdf"
                % (spacing/lam, target_theta, target_phi))


    # radiation pattern cross section plot
    plt.figure()
    plt.plot(dcx, afs_square_pow[int((len(dcx)-1)/2+1),:])
    plt.suptitle("Cross Section of Square Array Factor")
    plt.title("$d=%.2f\,\\lambda$, $\\theta_d=%.2f$°,$\\phi_d=%.2f$°"
              % (spacing / lam, target_theta, target_phi))
    plt.ylabel("$20\\log_{10}{(AF)}$")
    plt.xlabel("$\\sin{\\theta}\\cos{\\phi}$")
    plt.savefig("outputs/square-%.2f-lambda-%.2f-theta-%.2f-phi-cross.pdf"
                % (spacing/lam, target_theta, target_phi))

    plt.figure()
    plt.plot(dcx, afs_square_pow[int((len(dcx)-1)/2+1),:])
    plt.suptitle("Cross Section of Equilateral Array Factor")
    plt.title("$d=%.2f\,\\lambda$, $\\theta_d=%.2f$°,$\\phi_d=%.2f$°"
              % (spacing / lam, target_theta, target_phi))
    plt.ylabel("$20\\log_{10}{(AF)}$")
    plt.xlabel("$\\sin{\\theta}\\cos{\\phi}$")
    plt.savefig("outputs/equilat-%.2f-lambda-%.2f-theta-%.2f-phi-cross.pdf"
                % (spacing/lam, target_theta, target_phi))


    # geometry plot
    plt.figure()
    plt.tight_layout()
    plt.scatter(square_array.pos.real / lam,
                square_array.pos.imag / lam,
                marker="X", s=100)
    plt.suptitle("Square %dx%d Array Geometry"
                 % (square_array.size))
    plt.title("$d=%.2f\,\\lambda$, $\\theta_d=%.2f$°,$\\phi_d=%.2f$°"
              % (spacing / lam, target_theta, target_phi))
    plt.xlabel("x / $\\lambda$")
    plt.ylabel("y / $\\lambda$")
    # add phase numbers as text
    plot_phase_numbers(square_array, target_theta, target_phi, lam)
    plt.xlim([-1.4, 1.4])
    plt.ylim([-1.4, 1.4])
    plt.savefig("outputs/square-%.2f-lambda-%.2f-theta-%.2f-phi-geometry.pdf"
                % (spacing/lam, target_theta, target_phi))

    plt.figure()
    plt.tight_layout()
    plt.scatter(equilat_array.pos.real / lam,
                equilat_array.pos.imag / lam,
                marker="X", s=100)
    plt.suptitle("Equilateral %d-Antenna Array Geometry"
                 % (np.prod(square_array.size)))
    #plt.title("$d=%.2f\,\\lambda$, $\\theta_d=%.2f$°,$\\phi_d=%.2f$°"
    #          % (spacing / lam, target_theta, target_phi))
    plt.title("$d=%.2f\,\\lambda$" % (spacing / lam))
    plt.xlabel("x / $\\lambda$")
    plt.ylabel("y / $\\lambda$")
    plt.axis('equal')
    # add phase numbers as text
    #plot_phase_numbers(equilat_array, target_theta, target_phi, lam)
    plt.xlim([-1.4, 1.4])
    plt.ylim([-1.4, 1.4])
    plt.savefig("outputs/equilat-%.2f-lambda-%.2f-theta-%.2f-phi-geometry.pdf"
                % (spacing/lam, target_theta, target_phi))

    plt.show()


if __name__ == "__main__":
    main()

