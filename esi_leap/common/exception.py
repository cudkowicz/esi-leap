#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from esi_leap.common.i18n import _


class ESILeapException(Exception):
    msg_fmt = _("An unknown exception occurred.")
    code = 500
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                message = self.msg_fmt

        self.message = message
        super(ESILeapException, self).__init__(message)


class ContractNoPermission(ESILeapException):
    msg_fmt = _("You do not have permissions on "
                "contract %(contract_uuid)s.")


class ContractDuplicateName(ESILeapException):
    msg_fmt = _("Duplicate contracts with name %(name)s.")


class ContractNotFound(ESILeapException):
    msg_fmt = _("Contract with name or uuid %(contract_id)s not found.")


class ContractNoOfferUUID(ESILeapException):
    msg_fmt = _("Cannot create contract without parameter offer_uuid.")


class OfferNoPermission(ESILeapException):
    msg_fmt = _("You do not have permissions on "
                "offer %(offer_uuid)s.")


class OfferDuplicateName(ESILeapException):
    msg_fmt = _("Duplicate offers with name %(name)s.")


class OfferNotFound(ESILeapException):
    msg_fmt = _("Offer with name or uuid %(offer_uuid)s not found.")


class OfferNoTimeAvailabilities(ESILeapException):
    msg_fmt = _("Offer %(offer_uuid)s has no availabilities at given "
                "time range %(start_time)s, %(end_time)s.")


class OfferResourceTimeConflict(ESILeapException):
    msg_fmt = ("Offer on %(resource_type)s %(resource_uuid)s cannot be "
               "created with a start_time and end_time "
               "which conflicts with the time range of an existing offer "
               "on %(resource_type)s %(resource_uuid)s.")


class OfferNotAvailable(ESILeapException):
    msg_fmt = _("Offer %(offer_uuid)s does not have status "
                "'available'. Got offer status '%(status)s'.")


class ProjectNoPermission(ESILeapException):
    msg_fmt = _("You do not have permissions on project %(project_id)s.")


class ResourceNoPermission(ESILeapException):
    msg_fmt = _("You do not have permissions on "
                "%(resource_type)s %(resource_uuid)s.")


class ResourceTypeUnknown(ESILeapException):
    msg_fmt = _("%(resource_type)s resource type unknown.")


class InvalidTimeAPICommand(ESILeapException):
    msg_fmt = _("Attempted to get %(resource)s resource without providing "
                "both a valid Start Time and End Time. "
                "Start Time must be strictly less than End Time. "
                "Got %(start_time)s, %(end_time)s")


class InvalidAvailabilityAPICommand(ESILeapException):
    msg_fmt = _("Attempted to get an offer resource without providing "
                "both a valid Availability Start Time and Availability "
                "End Time. Availability Start Time must be strictly "
                "less than Availability End Time. "
                "Got %(a_start)s, %(a_end)s")


class InvalidTimeRange(ESILeapException):
    msg_fmt = _("Attempted to create %(resource)s resource with an invalid "
                "Start Time %(start_time)s and End Time %(end_time)s.")
