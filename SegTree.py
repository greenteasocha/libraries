import time
INF = float("inf")
MOD = 998244353


class LazySegmentTree():
    def __init__(self, n, uv, ux, vv, xv, xx, arr=[]):
        self.uv = uv  # unit of val
        self.ux = ux  # unit of lazy
        self.vv = vv  # function (v, v) => v
        self.xv = xv  # function (x, v) => v
        self.xx = xx  # function (x, x) => x

        # define size as power of two
        self.size = 1
        while (n):
            self.size <<= 1
            n //= 2

        # range size for each node
        self.width = [0]  # 1-index
        width = self.size
        while width:
            for i in range(self.size // width):
                self.width.append(width)
            width //= 2

        # initialize values
        if arr:
            self._init_arr(arr)
        else:
            self.val = [self.uv()] * (self.size << 1 | 1)
            self.lazy = [self.ux()] * (self.size << 1 | 1)

        return

    def _init_arr(self, arr):
        self.val = [self.uv()] * (self.size << 1 | 1)
        for i, val in enumerate(arr):
            self.val[i + self.size] = val
        self.lazy = [self.ux()] * (self.size << 1 | 1)

        self.ascend_all_val()

    def _resolve(self, k):
        # ex.
        # range add => return val + lazy
        # range affine => return val * lazy[0] + lazy[1]
        # ↑ (?)

        # return self.val[k] + self.lazy[k]
        return (self.val[k] * self.lazy[k][0] + self.lazy[k][1] * self.width[k])

    def _get_update_indices(self, l, r, order='descend'):
        # descending order
        l += self.size
        r += self.size - 1
        blen = r.bit_length()
        ret = []

        # lm = (l // (l & -l))
        # rm = (r // (r & -r))
        if order == 'descend':
            for i in range(blen + 1):
                # while l:
                # if r <= rm:
                ret.append(r >> i)
                # if l <= lm:
                ret.append(l >> i)

                # l //= 2
                # r //= 2
            return ret

        elif order == "ascend":
            for i in range(blen - 1, -1, -1):
                ret.append(r >> i)
                ret.append(l >> i)

            return ret

        else:
            assert 0, "invalid order."

    def _single_update(self, k):
        if k < self.size:
            l_val = self._resolve(k << 1)
            r_val = self._resolve(k << 1 | 1)

            self.val[k] = self.vv(l_val, r_val)

    def range_query(self, l, r):
        # resolve lazy values in top-down order
        update_indices = self._get_update_indices(l, r, "descend")
        revupdate_indices = self._get_update_indices(l, r, "ascend")
        for k in revupdate_indices:
            k_val, k_lazy, k_width = self.val[k], self.lazy[k], self.width[k]
            self.val[k] = self.xv(k_val, k_lazy, k_width)
            if k < self.size:
                lazy_val = self.lazy[k]

                c_lazy1 = self.lazy[k << 1]
                self.lazy[k << 1] = self.xx(k_lazy, c_lazy1)

                c_lazy2 = self.lazy[k << 1 | 1]
                self.lazy[k << 1 | 1] = self.xx(k_lazy, c_lazy2)

            self.lazy[k] = self.ux()

        # same as default segment tree query
        l += self.size
        r += self.size

        ret = self.uv()
        while l < r:
            if r & 1:
                r -= 1
                ret = self.vv(ret, self._resolve(r))
            if l & 1:
                ret = self.vv(ret, self._resolve(l))
                l += 1

            l >>= 1
            r >>= 1

        return ret

    def range_update(self, l, r, *v):
        # resolve lazy values in top-down order
        update_indices = self._get_update_indices(l, r, "descend")
        revupdate_indices = self._get_update_indices(l, r, "ascend")
        for k in revupdate_indices:
            k_val, k_lazy, k_width = self.val[k], self.lazy[k], self.width[k]
            self.val[k] = self.xv(k_val, k_lazy, k_width)
            if k < self.size:
                lazy_val = self.lazy[k]

                c_lazy1 = self.lazy[k << 1]
                self.lazy[k << 1] = self.xx(k_lazy, c_lazy1)

                c_lazy2 = self.lazy[k << 1 | 1]
                self.lazy[k << 1 | 1] = self.xx(k_lazy, c_lazy2)

            self.lazy[k] = self.ux()

        # set lazy values
        l += self.size
        r += self.size
        while l < r:
            if r & 1:
                r -= 1
                c_lazy = self.lazy[r]
                self.lazy[r] = self.xx(v, c_lazy)
            if l & 1:
                c_lazy = self.lazy[l]
                self.lazy[l] = self.xx(v, c_lazy)
                l += 1

            l >>= 1
            r >>= 1

        # update real value in bottom-up order
        for k in update_indices:
            if k < self.size:
                l_val = self._resolve(k << 1)
                r_val = self._resolve(k << 1 | 1)

                self.val[k] = self.vv(l_val, r_val)

    def show_val(self):
        idx = 1
        while idx <= self.size:
            print(self.val[idx:idx << 1])
            idx *= 2

    def show_lazy(self):
        idx = 1
        while idx <= self.size:
            print(self.lazy[idx:idx << 1])
            idx *= 2

    def ascend_all_val(self):
        for i in range(self.size << 1 - 1, -1, -1):
            self._single_update(i)
        return


def main():
    n, m = list(map(int, input().split()))

    def vv(l_val, r_val):
        # (val, val) => val
        return (l_val + r_val) % MOD

    def xv(val, lazy, range_size=1):
        # (val, lazy) => val
        return (val * lazy[0] + lazy[1] * range_size) % MOD

    def xx(p_lazy, c_lazy):
        # (lazy, lazy) => lazy
        return [
            (p_lazy[0] * c_lazy[0]) % MOD,
            (p_lazy[0] * c_lazy[1] + p_lazy[1]) % MOD
        ]

    def uv():
        # initial(unit) value
        return 0

    def ux():
        # initial(unit) lazy
        return [1, 0]

    arr = list(map(int, input().split()))
    st = LazySegmentTree(n, uv, ux, vv, xv, xx, arr)
    sec = time.time()

    ans = []
    for i in range(m):
        q, *param = list(map(int, input().split()))
        if q == 0:
            st.range_update(*param)
        else:
            v = st.range_query(*param)
            ans.append(v % MOD)

    print(*ans, sep="\n")

    # print(time.time() - sec)
    return 0


if __name__ == "__main__":
    main()
