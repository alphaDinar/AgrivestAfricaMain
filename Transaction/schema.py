from Log.models import User,Balance,Wallet
from Asset.models import Partner,Trade,Farm,Produce
from .models import TradeInvoice,FarmInvoice,ProduceInvoice
import graphene
from graphene_django import DjangoObjectType,DjangoListField

class UserData(DjangoObjectType):
   class Meta:
      model = User

class BalanceData(DjangoObjectType):
   class Meta:
      model = Balance

class WalletData(DjangoObjectType):
   class Meta:
      model = Wallet

class PartnerData(DjangoObjectType):
   class Meta:
      model = Partner

class TradeData(DjangoObjectType):
   class Meta:
      model = Trade

class TradeInvoiceData(DjangoObjectType):
  class Meta:
      model = TradeInvoice

class FarmData(DjangoObjectType):
   class Meta:
      model = Farm

class FarmInvoiceData(DjangoObjectType):
   class Meta:
      model = FarmInvoice

class ProduceData(DjangoObjectType):
   class Meta:
      model = Produce

class ProduceInvoiceData(DjangoObjectType):
   class Meta:
      model = ProduceInvoice

class Query(graphene.ObjectType):
   all_users = DjangoListField(UserData)
   all_balances = DjangoListField(BalanceData)
   all_wallets = DjangoListField(WalletData)

   all_partners = DjangoListField(PartnerData)    
   all_trades = DjangoListField(TradeData)
   all_trade_invoices= DjangoListField(TradeInvoiceData)
   get_trade_invoice = graphene.Field(TradeInvoiceData, id = graphene.Int(required = True))
   def resolve_get_trade_invoice(root, info, id):
      return TradeInvoice.objects.get(id=id)
   
   all_farms = DjangoListField(FarmData)
   get_farm = graphene.Field(FarmData, id=graphene.Int(required=True))
   def resolve_get_farm(root, info ,id):
      return Farm.objects.get(id=id)
   all_farm_invoices = DjangoListField(FarmInvoiceData)
   get_farm_invoice = graphene.Field(FarmInvoiceData, id=graphene.Int(required=True))
   def resolve_get_farm_invoice(root, info, id):
      return FarmInvoice.objects.get(id=id)
   
   all_produces = DjangoListField(ProduceData)
   all_produce_invoices = DjangoListField(ProduceInvoiceData)


class CompleteTradeMutation(graphene.Mutation):
   class Arguments:
      id = graphene.Int()
   tradeInvoice = graphene.Field(TradeInvoiceData)
   def mutate(root, info, id):
      tradeInvoiceObj = TradeInvoice.objects.get(id=id)
      tradeInvoiceObj.status = 'Completed'
      tradeInvoiceObj.save()
      return CompleteTradeMutation(tradeInvoice=tradeInvoiceObj)
   
class CreateBalances(graphene.Mutation):
   class Arguments:
      id = graphene.Int()
   balance = graphene.Int()
   def mutate(root, info, id):
      users = User.objects.all()
      for user in users:
         if not Balance.objects.filter(id=user).exists():
            Balance.objects.create(user=user.id)
      return CreateBalances(balance=2)

class changePayoutMutation(graphene.Mutation):
   class Arguments:
      id = graphene.Int()
      payout = graphene.Float()
   farm = graphene.Field(FarmData)
   def mutate(root, info, id, payout):
      farm = Farm.objects.get(id=id)
      farm.payout = payout
      farm.save()
      return changePayoutMutation(farm=farm)

class Mutation(graphene.ObjectType):
   complete_trade = CompleteTradeMutation.Field()
   change_payout = changePayoutMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)