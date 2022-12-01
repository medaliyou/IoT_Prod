import asyncio
from common.Defines import S_RANDOM_NUMBER, S_KEY, ErrorModel
from common.X import X, XOps
from common.base_logger import logger
from stubs.RA import cRAClient


class SD(object):
    def __init__(self, TAG_SD: str = None):

        self.TAG_SD: str = TAG_SD

        self.ID_SD: X = None
        self.K_SD: X = None

        self.r_SD: X = None
        self.RN_SD: X = None
        self.PID_SD: X = None

        self.K_G_SD: X = None

        self.B1: X = None
        self.B2: X = None

        # Session Key
        self.SK: X = None

        # Auth S3
        self.V_G_MU: X = None
        self.PID_MU: X = None
        self.C2: X = None
        self.M3: X = None
        self.M4: X = None
        self.V_SD: X = None

    def export_dict(self):
        _dict = self.__dict__
        _masked_keys = ["TAG_SD"]
        # logger.info(_dict)

        try:
            for k in _dict:
                # logger.info("{}={}".format(k, _dict[k]))
                if k not in _masked_keys:
                    if isinstance(_dict[k], X):
                        _dict[k] = _dict[k].h
            return _dict

        except Exception as e:
            logger.error(e)

    def import_dict(self, dict_obj):
        _dict = {}
        _masked_keys = ["TAG_SD"]
        try:
            for k in dict_obj:
                # logger.warning("{} = {}".format(k, dict_obj[k]))
                if k not in _masked_keys:
                    # if isinstance(dict_obj[k], X):
                    _dict[k] = X(h=dict_obj[k])
                else:
                    _dict[k] = dict_obj[k]
            # logger.warning(self.__dict__)
            self.__dict__.update(_dict)
        except Exception as e:
            logger.error(e)
            logger.error("dict key {}".format(k))

    def __generate_r(self):
        self.r_SD = X(s=S_RANDOM_NUMBER)  # 128 bits Random Number

    def __generate_K(self):
        self.K_SD = X(s=S_KEY)  # 128 bits Random Number

    def __generate_RN(self):
        self.RN_SD = X(s=S_RANDOM_NUMBER)

    def __compute_PID(self):
        """
        Computes PIDSD = h( IDSD ||rSD )
        :return:
        """
        # __concat = Ops.ops_concatenate(self.ID, self.r)
        self.PID_SD = XOps.hash(self.ID_SD + self.r_SD)

    async def init_phase(self):
        _RA_Client = await cRAClient()
        response = await _RA_Client.GetID()
        if response is not None:
            self.ID_SD = X(h=response.ID)
            self.__generate_r()
            self.__generate_K()
            self.__compute_PID()
            logger.info("ID_SD={}".format(self.ID_SD.h))

    async def register_phase(self):
        _RA_Client = await cRAClient()
        response = await _RA_Client.RegisterSD(self.ID_SD.h, self.PID_SD.h, self.r_SD.h)
        if response is not None:
            self.K_G_SD = X(h=response.K_G)
            logger.info("K_G_SD={}".format(self.K_G_SD.h))
            self.process_register_phase()

    def process_register_phase(self):

        # B1 = rSD ⊕ h( IDSD ||KSD )
        self.B1 = self.r_SD ^ (XOps.hash(self.ID_SD + self.K_SD))
        # B2 = KGSD ⊕ h(rSD ||KSD )
        self.B2 = self.K_G_SD ^ XOps.hash(self.r_SD + self.K_SD)
        # Stores { B1 , B2 , PIDSD } in the memory
        registration_state = {
            "B1": self.B1,
            "B2": self.B2,
            "PID": self.PID_SD
        }
        logger.warning(registration_state)

    async def process_auth_KE_S3(self, PID, M3, C2, V):
        try:
            self.PID_MU = X(h=PID)
            self.M3 = X(h=M3)
            self.C2 = X(h=C2)
            self.V_G_MU = X(h=V)

            # Computes
            # rSD = B1 ⊕ h( IDSD ||KSD )
            _r_SD = self.B1 ^ XOps.hash(self.ID_SD + self.K_SD)

            # KGSD = B2 ⊕ h(rSD ||KSD )
            self.K_G_SD = self.B2 ^ XOps.hash(_r_SD + self.K_SD)

            # M2∗ = M3 ⊕ h( PIDSD ||KGSD ||rSD )
            _M2_star = self.M3 ^ XOps.hash(self.PID_SD + self.K_G_SD + _r_SD)
            # VMUG* = h( PID MU || M2∗ ||KGSD )
            _V_G_MU_star = XOps.hash(self.PID_MU + _M2_star + self.K_G_SD)

            # Checks VMUG* = VMUG

            logger.warning(
                "Checks VMUG* == VMUG"
            )
            logger.warning(
                "VMUG* = {}".format(_V_G_MU_star.h)
            )
            logger.warning(
                "VMUG = {}".format(self.V_G_MU)
            )

            if _V_G_MU_star != self.V_G_MU:
                # Verification not successful

                return ErrorModel(1, "V_G_MU* verification failed")

            # return ErrorModel(0, "V_G_MU* verification success!")

            # Indicate to Backend that Registration Was OK
            # and continue calculation

            # Generates RNSD
            self.__generate_RN()

            # Computes
            # (h( ID MU || RNMU )||h( IDG || RNG )) = C2 ⊕ h(KGSD ||rSD )
            _hash_IDMU_RNMU_c_hash_IDG_RNG = self.C2 ^ XOps.hash(self.K_G_SD + _r_SD)

            # SK = h( h( ID MU || RNMU )||h( IDG || RNG ) || h( IDSD || RNSD ))
            self.SK = XOps.hash(
                _hash_IDMU_RNMU_c_hash_IDG_RNG + XOps.hash(self.ID_SD + self.RN_SD)
            )
            logger.warning("\n[SESSION KEY]={}".format(self.SK))

            # M4 = h( PIDSD ||KGSD ||rSD ) ⊕ h( IDSD || RNSD )
            self.M4 = XOps.hash(self.PID_SD + self.K_G_SD + _r_SD) ^ XOps.hash(self.ID_SD + self.RN_SD)

            # VSD = h( PID MU || PIDSD || M2∗ ||h( IDSD || RNSD )||KGSD )
            self.V_SD = XOps.hash(
                self.PID_MU + self.PID_SD + _M2_star + XOps.hash(self.ID_SD + self.RN_SD) + self.K_G_SD)

            authentication_state = {
                "M4": self.M4,
                "V": self.V_SD,
                "PID": self.PID_SD
            }
            return self.M4, self.V_SD


        except Exception as e:
            logger.error(e)


async def main(_SD_Instance: SD):
    await _SD_Instance.init_phase()
    await asyncio.sleep(0.001)
    await _SD_Instance.register_phase()
    # asyncio.sleep(0.5)


if __name__ == '__main__':
    SD_Instance = SD()
    asyncio.run(main(SD))
