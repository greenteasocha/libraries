INF = float("inf")
MOD = 998244353


class LazySegmentTree():
    def __init__(self, n):
        # define size as power of two
        self.size = 1
        while (n):
            self.size <<= 1
            n //= 2

        # initialize values
        self.val = [self._unit_val()] * (self.size * 2 + 1)
        self.lazy = [self._unit_lazy()] * (self.size * 2 + 1)

        # range size for each node
        self.width = [0]  # 1-index
        width = self.size
        while width:
            for i in range(self.size // width):
                self.width.append(width)
            width //= 2

        return

    def init_arr(self, arr):
        for i, val in enumerate(arr):
            self.val[i + self.size] = val
        # self.val = [self._unit_val()] * (self.size + 1) + arr
        self.lazy = [self._unit_lazy()] * (self.size * 2 + 1)
        self.update_all()

    def _operation(self, l_val, r_val):
        # ex.
        # range sum => return l_val + r_val
        # range min => return min(l_val, r_val)
        return (l_val + r_val)

    def _resolve(self, k):
        # ex.
        # range add => return val + lazy
        # range affine => return val * lazy[0] + lazy[1]
        # ↑ (?)

        # return self.val[k] + self.lazy[k]
        return (self.val[k] * self.lazy[k][0] + self.lazy[k][1])

    def _distribute(self, k, lazy_val):
        # self.lazy[k * 2] += lazy_val // 2
        # self.lazy[k * 2 + 1] += lazy_val // 2
        lazy1 = self.lazy[k * 2]
        self.lazy[k * 2] = [(lazy1[0] * lazy_val[0]),
                            (lazy1[1] * lazy_val[0] + lazy_val[1] // 2)]

        lazy2 = self.lazy[k * 2 + 1]
        self.lazy[k * 2 + 1] = [(lazy2[0] * lazy_val[0]),
                                (lazy2[1] * lazy_val[0] + lazy_val[1] // 2)]

    def _unit_val(self):
        # initial(unit) value
        return 0

    def _unit_lazy(self):
        # initial(unit) value of lazy
        # return 0
        return [1, 0]

    def _get_update_indices(self, l, r):
        # descending order
        l += self.size
        r += self.size - 1
        ret = []
        # lm = (l // (l & -l))
        # rm = (r // (r & -r))

        while l:
            # if r <= rm:
            ret.append(r)
            # if l <= lm:
            ret.append(l)

            l //= 2
            r //= 2
        return ret

    def _single_update(self, k):
        if k < self.size:
            l_val = self._resolve(k * 2)
            r_val = self._resolve(k * 2 + 1)
            self.val[k] = self._operation(l_val, r_val)

    def _unlazy(self, k):
        self.val[k] = self._resolve(k)
        if k < self.size:
            lazy_val = self.lazy[k]
            self._distribute(k, lazy_val)

        self.lazy[k] = self._unit_lazy()

    def range_query(self, l, r):
        # resolve lazy values in top-down order
        for k in reversed(self._get_update_indices(l, r)):
            self._unlazy(k)

        # same as default segment tree query
        l += self.size
        r += self.size

        ret = 0
        while l < r:
            if r & 1:
                r -= 1
                # self._unlazy(r)
                ret = self._operation(ret, self._resolve(r))
            if l & 1:
                # self._unlazy(l)
                ret = self._operation(ret, self._resolve(l))
                l += 1

            l >>= 1
            r >>= 1

        return ret

    def range_update(self, l, r, v):
        # resolve lazy values in top-down order
        update_indices = self._get_update_indices(l, r)
        for k in reversed(update_indices):
            self._unlazy(k)

        # set lazy values
        l += self.size
        r += self.size
        while l < r:
            if r & 1:
                r -= 1
                # self.lazy[r] += v * self.width[r]
                self.lazy[r] = [
                    self.lazy[r][0] * v[0],
                    (self.lazy[r][1] * v[0] + v[1]) * self.width[r]
                ]
            if l & 1:
                self.lazy[l] = [
                    self.lazy[l][0] * v[0],
                    (self.lazy[l][1] * v[0] + v[1]) * self.width[l]
                ]
                l += 1

            l >>= 1
            r >>= 1

        # update real value in bottom-up order
        for k in update_indices:
            self._single_update(k)

    def show_val(self):
        idx = 1
        while idx <= self.size:
            print(self.val[idx:idx * 2])
            idx *= 2

    def show_lazy(self):
        idx = 1
        while idx <= self.size:
            print(self.lazy[idx:idx * 2])
            idx *= 2

    def update_all(self):
        for i in range(1, self.size * 2):
            self._unlazy(i)

        for i in range(self.size * 2 - 1, -1, -1):
            self._single_update(i)
        return


def main():
    n, m = list(map(int, input().split()))
    st = LazySegmentTree(n)
    st.init_arr(list(map(int, input().split())))

    for i in range(m):
        # st.update_all()
        q = list(map(int, input().split()))
        if q[0] == 0:

            st.range_update(q[1], q[2], [q[3], q[4]])
            st.update_all()
        else:

            v = st.range_query(q[1], q[2])
            print(v % MOD)
        # st.show_val()
        # st.show_lazy()

    return 0


if __name__ == "__main__":
    main()