def gen_plotter(f):
    def wrapper(ax_artists):
        [ax, artists] = ax_artists
        new_artist = f(ax)

        if new_artist is not None:
            artists.append(new_artist)
        return (ax, artists)
    return wrapper
