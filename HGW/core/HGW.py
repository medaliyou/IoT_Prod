from common.Defines import S_ID, S_RANDOM_NUMBER, ErrorModel
from common.SingletonMeta import SingletonMeta
from common.X import X, XOps
from common.base_logger import logger
from database.MU import retrieve_MU_by_PID, update_MU
from database.SD import retrieve_SD_by_PID
from stubs.SD import cSDClient


class HGW(metaclass=SingletonMeta):

    def __init__(self):
        # HGW
        self.SK: X = None
        self.ID_HGW: X = None
        self.RN_HGW: X = None

        # SD
        self.ID_SD: X = None
        self.K_G_SD: X = None
        self.PID_SD: X = None
        self.r_SD: X = None
        # MU
        self.K_G_MU: X = None
        self.ID_MU: X = None
        self.RN_MU: X = None
        self.RID_MU: X = None
        self.PID_MU: X = None
        self.RID_MU_new: X = None
        self.PID_MU_new: X = None

        self.M1: X = None
        self.V: X = None
        self.C1: X = None

        self.M3: X = None
        self.C2: X = None
        self.V_G_MU: X = None
        self.M2: X = None
        self.SD: X = None
        self.M4: X = None
        self.V_SD: X = None
        self.M5: X = None
        self.V_G_SD: X = None
        self.M6: X = None

        self.__init_ID()

    def __init_ID(self):
        self.ID_HGW = X(s=S_ID)

    def __generate_RN(self):
        self.RN_HGW = X(s=S_RANDOM_NUMBER)

    async def __get_corresponding_SD(self, PID):
        logger.debug("Retrieving SD")
        _SD = await retrieve_SD_by_PID(PID)
        if _SD is not None:
            logger.debug(_SD)
            return _SD

    async def __update_MU_PIDn_RIDn(self, PID_MU, PID_MU_new, RID_MU_new):
        try:
            # retrieve
            _MU = await retrieve_MU_by_PID(PID_MU=PID_MU)
            if _MU is None:
                return ErrorModel(1, "Empty MU corresponding to PID_MU")

            exclude_keys = ["id"]
            _MU_copy = {k: _MU[k] for k in set(list(_MU.keys())) - set(exclude_keys)}

            _MU_copy["PID_n"] = PID_MU_new
            _MU_copy["RID_n"] = RID_MU_new
            # update
            res = await update_MU(_MU["id"], _MU_copy)
            if res:
                return ErrorModel(0, "Updated MU {PID_MU_new, RID_MU_new}")
            else:
                return ErrorModel(1, "Updated MU failed")

        except Exception as e:
            logger.error(e)

    async def __update_MU_PID_RID(self, PID_MU):
        # If it is correct, deletes { PID MU , RID MU } in the database
        try:
            _MU = await retrieve_MU_by_PID(PID_MU=PID_MU)
            if _MU is None:
                return ErrorModel(1, "Empty MU corresponding to PID_MU")

            exclude_keys = ["id"]
            _MU_copy = {k: _MU[k] for k in set(list(_MU.keys())) - set(exclude_keys)}

            _MU_copy["PID"] = _MU_copy["PID_n"]
            _MU_copy["RID"] = _MU_copy["RID_n"]
            _MU_copy["PID_n"] = ""
            _MU_copy["RID_n"] = ""

            res = await update_MU(_MU["id"], _MU_copy)
            if res:
                return ErrorModel(0, "Deleted {PID_MU, RID_MU} from database (replaced with {PID_MU_new, RID_MU_new})")
            else:
                return ErrorModel(1, "Deleted {PID_MU, RID_MU} failed")

        except Exception as e:
            logger.error(e)

    async def process_auth_KE(self, MU, MU_Auth) -> (X, X):
        ret = await self.process_auth_KE_S2(MU, MU_Auth)
        if ret.err_no == 0:
            return await self.process_auth_KE_S4()

    async def process_auth_KE_S2(self, MU, MU_Auth) -> ErrorModel:
        try:
            # Retrieves RID MU and K MUG corresponding to PID MU
            self.ID_MU = X(h=MU["ID"])
            self.PID_MU = X(h=MU["PID"])
            self.K_G_MU = X(h=MU["K_G"])

            self.RID_MU = X(h=MU["RID"])

            self.M1 = X(h=MU_Auth["M1"])

            self.V = X(h=MU_Auth["V"])

            self.C1 = X(h=MU_Auth["C1"])

            logger.warning(MU)
            logger.warning(MU_Auth)

            # ( RN_HGW*MU || PID∗SD ) = M1 ⊕ h ( PID MU || RID MU || K MUG )
            # __concat_RN_MU_star_PID_MU_star
            _c_RNMU_star_PIDSD_star = self.M1 ^ XOps.hash(self.PID_MU + self.RID_MU + self.K_G_MU)
            logger.warning("_c_RNMU_star_PIDSD_star = {}".format(_c_RNMU_star_PIDSD_star))

            len_concat = len(_c_RNMU_star_PIDSD_star.b)
            logger.warning("len_concat = {}".format(len_concat))

            # Make sure l % 2 == 0
            assert len_concat & 1 == 0

            _RN_MU_star = X(b=_c_RNMU_star_PIDSD_star.b[:S_ID])  # 16 bytes sizeof (RN_MU)
            _PID_SD_star = X(b=_c_RNMU_star_PIDSD_star.b[S_ID:])

            # V*MU = h ( PID MU || RID MU || RN_HGW*MU || PID*SD || K MUG )
            _V_MU_star = XOps.hash(self.PID_MU + self.RID_MU + _c_RNMU_star_PIDSD_star + self.K_G_MU)

            # Checks V_MU∗ = V_MU
            logger.warning(
                "Checks V_MU∗ == V_MU"
            )
            logger.warning(
                "V_MU∗ = {}".format(_V_MU_star)
            )
            logger.warning(
                "V_MU = {}".format(self.V)
            )

            if _V_MU_star != self.V:
                return ErrorModel(1, "V_MU* Check failed")

            # Retrieves KGSD and rSD corresponding to PIDSD
            self.SD = await self.__get_corresponding_SD(_PID_SD_star.h)

            assert self.SD is not None
            self.ID_SD = X(h=self.SD["ID"])
            self.PID_SD = X(h=self.SD["PID"])
            self.K_G_SD = X(h=self.SD["K_G"])
            self.r_SD = X(h=self.SD["r"])

            # Generates RNG
            self.__generate_RN()

            # Computes
            # M2 = h( RNMU || RNG )
            self.M2 = XOps.hash(_RN_MU_star + self.RN_HGW)

            # M3 = h( PIDSD ||KGSD ||rSD ) ⊕ M2
            self.M3 = XOps.hash(self.PID_SD + self.K_G_SD + self.r_SD) ^ self.M2

            # h( ID MU || RNMU ) = C1 ⊕ h(K MUG || RNMU )
            _hash_IDMU_RNMU = self.C1 ^ XOps.hash(self.K_G_MU + _RN_MU_star)

            # C2 = (h( ID MU || RNMU )||h( IDG || RNG )) ⊕ h(KGSD ||rSD )
            self.C2 = (_hash_IDMU_RNMU + XOps.hash(self.ID_HGW + self.RN_HGW) + XOps.hash(self.K_G_SD + self.r_SD))

            # VMUG = h( PID MU || M2 ||KGSD )
            self.V_G_MU = XOps.hash(self.PID_MU + self.M2 + self.K_G_SD)

            '''
                Save the Objects context from the first Request
            '''

            self.RN_MU = _RN_MU_star
            # Update S2
            S2 = {
                "ID_MU": self.ID_MU,
                "PID_MU": self.PID_MU,
                "K_G_MU": self.K_G_MU,
                "RID_MU": self.RID_MU,
                "RN_MU": _RN_MU_star,
                "M2": self.M2,
                "M3": self.M3,
                "C2": self.C2,
                "V_G": self.V_G_MU

            }

            auth_KE_S2_state = {
                "PID": self.PID_MU.h,
                "M3": self.M3.h,
                "C2": self.C2.h,
                "V_G": self.V_G_MU.h
            }

            logger.info(auth_KE_S2_state)
            _SD_Client = await cSDClient()

            response = await _SD_Client.AuthKES3(PID_MU=self.PID_MU.h, C2=self.C2.h, M3=self.M3.h, V_G_MU=self.V_G_MU.h)
            if response is not None:
                logger.warning(response)
                self.M4 = X(h=response.M4)
                self.V_SD = X(h=response.V)

                return ErrorModel(0, "OK")

        except Exception as e:
            logger.error(e)
            return ErrorModel(1, e)

    async def process_auth_KE_S4(self) -> (X, X):
        try:

            # Computes
            # h( IDSD || RNSD ) = M4 ⊕ h( PIDSD ||KGSD ||rSD )
            _hash_ID_SD_concat_RN_SD = self.M4 ^ XOps.hash(self.PID_SD + self.K_G_SD + self.r_SD)
            # VSD* = h(PIDMU || PIDSD || M2 || h ( IDSD || RNSD ) || K GSD )
            _V_SD_star = XOps.hash(self.PID_MU + self.PID_SD + self.M2 + _hash_ID_SD_concat_RN_SD + self.K_G_SD)
            # Checks VSD* = VSD ?

            logger.warning(
                "Checks VSD∗ == VSD"
            )
            logger.warning(
                "VSD∗ = {}".format(_V_SD_star)
            )
            logger.warning(
                "VSD = {}".format(self.V_SD)
            )

            if _V_SD_star != self.V_SD:
                logger.warning("VSD* != VSD")
                ErrorModel(1, "VSD* != VSD")

            # Computes
            # SK = h(h( ID MU || RNMU )||h( IDG || RNG )||h( IDSD || RNSD ))
            self.SK = XOps.hash(
                XOps.hash(self.ID_MU + self.RN_MU) + XOps.hash(
                    self.ID_HGW + self.RN_HGW) + _hash_ID_SD_concat_RN_SD
            )
            logger.warning("\n[SESSION KEY]={}".format(self.SK))

            # PID new  MU = h ( PID MU || RNMU )
            self.PID_MU_new = XOps.hash(self.PID_MU + self.RN_MU)

            # RID new MU = h ( PID MU || K MUG )
            self.RID_MU_new = XOps.hash(self.PID_MU + self.K_G_MU)

            # M5 = h( RID MU || RNMU ) ⊕ (h( IDG || RNG )||h( IDSD || RNSD )|| PID new )
            self.M5 = XOps.hash(self.RID_MU + self.RN_MU) ^ (
                    XOps.hash(self.ID_HGW + self.RN_HGW) + _hash_ID_SD_concat_RN_SD + self.PID_MU_new)

            # VGSD = h( PID MU || RNMU ||h( IDG || RNG )||h( IDSD || RNSD )|| PID new MU || K MUG )
            self.V_G_SD = XOps.hash(self.PID_MU + self.RN_MU + XOps.hash(
                self.ID_HGW + self.RN_HGW) + _hash_ID_SD_concat_RN_SD + self.PID_MU_new + self.K_G_MU)

            # Stores { PID MU , RID MU } with { PID new MU , RID new MU } in HGW’s database
            ret = await self.__update_MU_PIDn_RIDn(self.PID_MU.h, self.PID_MU_new.h, self.RID_MU_new.h)
            if ret.err_no == 0:
                logger.warning("Updated MU successfully S4.")

            else:
                logger.warning(ret)
                return ret

            # Sends { M5 ,VGSD } to MU

            '''
                Save the Objects context from the first Request
            '''
            # Update S2
            self.S4 = {
                "PID_MU_new": self.PID_MU_new,
                "RID_MU_new": self.RID_MU_new,
                "SK": self.SK,
                "V_SD_star": _V_SD_star,
                "_M5": self.M5,
                "V_G_SD": self.V_G_SD

            }
            self.auth_KE_S4_state = {
                "M5": self.M5.h,
                "V_G": self.V_G_SD.h,
            }

            return self.M5, self.V_G_SD

        except Exception as e:
            logger.error(e)

    async def process_auth_KE_S6(self, M6, PID_MU) -> ErrorModel:

        try:

            self.M6 = X(h=M6)
            self.PID_MU = X(h=PID_MU)

            # Computes
            # M6∗ = h(SK || PID new MU )
            _M6_star = XOps.hash(self.SK + self.PID_MU_new)

            # Checks M6∗ = M6 ?

            logger.warning(
                "Checks M6∗ == M6"
            )
            logger.warning(
                "M6∗ = {}".format(_M6_star)
            )
            logger.warning(
                "M6 = {}".format(self.M6)
            )

            if _M6_star != self.M6:
                return ErrorModel(1, "M6* != M6")

            # If it is correct, deletes { PID MU , RID MU } in the database

            ret = await self.__update_MU_PID_RID(self.PID_MU.h)
            if ret.err_no == 0:
                logger.warning("Updated MU successfully S6.")
                return ret
            else:
                logger.warning(ret)
                return ret

        except Exception as e:

            logger.error(e)
