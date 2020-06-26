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

import datetime
import pecan
from pecan import rest
import wsme
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from esi_leap.api.controllers import base
from esi_leap.api.controllers import types
from esi_leap.common import exception
from esi_leap.common import policy
from esi_leap.objects import offer
from esi_leap.resource_objects import resource_object_factory as ro_factory


class Offer(base.ESILEAPBase):

    uuid = wsme.wsattr(wtypes.text, readonly=True)
    project_id = wsme.wsattr(wtypes.text)
    resource_type = wsme.wsattr(wtypes.text, mandatory=True)
    resource_uuid = wsme.wsattr(wtypes.text, mandatory=True)
    start_time = wsme.wsattr(datetime.datetime)
    end_time = wsme.wsattr(datetime.datetime)
    status = wsme.wsattr(wtypes.text)
    properties = {wtypes.text: types.jsontype}

    def __init__(self, **kwargs):

        self.fields = offer.Offer.fields
        for field in self.fields:
            setattr(self, field, kwargs.get(field, wtypes.Unset))


class OfferCollection(types.Collection):
    offers = [Offer]

    def __init__(self, **kwargs):
        self._type = 'offers'


class OffersController(rest.RestController):

    @wsme_pecan.wsexpose(Offer, wtypes.text)
    def get_one(self, offer_uuid):
        request = pecan.request.context
        cdict = request.to_policy_values()
        policy.authorize('esi_leap:offer:get', cdict, cdict)

        o = offer.Offer.get(request, offer_uuid)
        return Offer(**o.to_dict())

    @wsme_pecan.wsexpose(OfferCollection, wtypes.text, wtypes.text,
                         wtypes.text, datetime.datetime, datetime.datetime,
                         wtypes.text)
    def get_all(self, project_id=None, resource_type=None,
                resource_uuid=None, start_time=None, end_time=None,
                status=None):

        request = pecan.request.context
        cdict = request.to_policy_values()
        policy.authorize('esi_leap:offer:get', cdict, cdict)

        if (start_time and end_time is None) or\
           (end_time and start_time is None):
            raise exception.InvalidTimeCommand(resource='an offer',
                                               start_time=str(start_time),
                                               end_time=str(end_time))

        possible_filters = {
            'project_id': project_id,
            'resource_type': resource_type,
            'resource_uuid': resource_uuid,
            'status': status,
            'start_time': start_time,
            'end_time': end_time,
        }

        filters = {}
        for k, v in possible_filters.items():
            if v is not None:
                filters[k] = v

        offer_collection = OfferCollection()
        offers = offer.Offer.get_all(request, filters)
        offer_collection.offers = [
            Offer(**o.to_dict()) for o in offers]
        return offer_collection

    @wsme_pecan.wsexpose(Offer, body=Offer)
    def post(self, new_offer):
        request = pecan.request.context
        cdict = request.to_policy_values()
        policy.authorize('esi_leap:offer:create', cdict, cdict)

        offer_dict = new_offer.to_dict()

        if 'project_id' in offer_dict:
            if offer_dict['project_id'] != request.project_id:
                policy.authorize('esi_leap:offer:offer_admin', cdict, cdict)
        else:
            offer_dict['project_id'] = request.project_id

        OffersController._verify_resource_permission(cdict, offer_dict)

        o = offer.Offer(**offer_dict)
        o.create(request)
        return Offer(**o.to_dict())

    @wsme_pecan.wsexpose(Offer, wtypes.text)
    def delete(self, offer_uuid):
        request = pecan.request.context
        cdict = request.to_policy_values()
        policy.authorize('esi_leap:offer:delete', cdict, cdict)

        o = offer.Offer.get(request, offer_uuid)
        OffersController._verify_resource_permission(cdict, o.to_dict())

        o.destroy()

    @staticmethod
    def _verify_resource_permission(cdict, offer_dict):
        resource_type = offer_dict.get('resource_type')
        resource_uuid = offer_dict.get('resource_uuid')
        resource = ro_factory.ResourceObjectFactory.get_resource_object(
            resource_type, resource_uuid)
        if not resource.is_resource_admin(offer_dict['project_id']):
            policy.authorize('esi_leap:offer:offer_admin', cdict, cdict)
